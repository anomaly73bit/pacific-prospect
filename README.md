# Pacific Prospect

Portale Jekyll di intelligence commerciale per Pacific IT Solutions, in italiano e responsive.

## Pubblicazione

Il workflow `.github/workflows/pages.yml` valida i dati, costruisce Jekyll e pubblica su GitHub Pages. Se il repository non ha ancora Pages attivo, selezionare **Settings → Pages → Source → GitHub Actions**. Dominio: https://prospect.pacificit.solutions/

Per un dominio personalizzato, configurare Pages e DNS, quindi cambiare `url` e impostare `baseurl: ""` in `_config.yml`.

## Catalogo e aggiornamento

- `_data/curated.json`: ricerca editoriale con fonti, ruoli e foto da pagine professionali pubbliche.
- `_data/boards.json`: elenco espandibile delle job board Ashby pubbliche. Nessun limite applicativo al numero di aziende configurabili.
- `scripts/refresh.py`: consulta le API pubbliche, deduplica per azienda e individua segnali database/cloud. Non raccoglie dati privati e non effettua scraping LinkedIn.
- `_data/companies.json`: catalogo effettivamente mostrato.
- `_data/meta.json`: esito della verifica, feed riusciti e falliti.

Aggiornamento quotidiano alle 06:23 UTC, tramite GitHub Actions (l'orario è indicativo). Per aggiornare subito: Actions → Refresh catalog and deploy Jekyll → Run workflow. Le esecuzioni schedulate GitHub possono subire ritardi o essere disabilitate per inattività. Le nuove aziende richiedono l'aggiunta di una job board o una scheda editoriale: il sistema non scopre automaticamente tutte le aziende del web.

Il catalogo è parziale, non un censimento mondiale. Le persone non documentate non sono inventate; LinkedIn e fotografie compaiono solo quando verificati. Le immagini sono caricate dai siti aziendali e possono diventare indisponibili. Un annuncio non equivale a interesse per servizi esterni; fornitori di database e cloud possono essere concorrenti o potenziali partner, da qualificare prima di contattarli.

## Punteggio

Somma euristica su 100: tecnologia 35, bisogno 25, remoto 25, apertura commerciale 15. La metodologia completa è disponibile nell'interfaccia. Il punteggio non rappresenta la probabilità di vendita. La località degli annunci non è necessariamente la sede legale. Le restrizioni di un annuncio di lavoro non sono automaticamente applicabili a un contratto di consulenza.

## Funzioni

Ricerca per nome, tecnologia e persona; filtri geografici, settore, tecnologia, remoto, contatti e compatibilità; ordinamento; scheda azienda; fonti e data; preferiti; stato commerciale; note; CSV; backup JSON e ripristino. I dati personali della pipeline sono salvati esclusivamente in localStorage, senza sincronizzazione fra dispositivi. Repository e catalogo sono pubblici, le note non vengono pubblicate.

## Sviluppo

Ruby + Bundler: `bundle install`, `bundle exec jekyll serve`. Python 3 (standard library): `python scripts/refresh.py`, `python scripts/validate.py`. JavaScript: `node --check assets/app.js`.
