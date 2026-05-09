# D&D 5e (Regole 2024) Character Builder

Benvenuto in questo progetto! Questa applicazione web permette di creare personaggi di Dungeons & Dragons basati sulle nuove regole del 2024. È pensata per essere facile da usare per i giocatori e facile da pubblicare (hostare) online per te.

Questa guida è stata scritta per aiutarti passo dopo passo a mettere online il progetto, anche se non hai mai programmato o usato questi strumenti prima d'ora!

---

## Passo 1: Creare un account su GitHub

GitHub è come un "Google Drive" per il codice dei programmatori. Ci servirà per salvare il tuo progetto online e per permettere a Streamlit (il servizio che creerà il sito web) di leggerlo.

1. Vai su [GitHub.com](https://github.com/).
2. Clicca sul pulsante **Sign up** (Iscriviti) in alto a destra.
3. Inserisci la tua email, scegli una password e un nome utente.
4. Segui le istruzioni a schermo per verificare che non sei un robot e completa la registrazione.
5. Controlla la tua email per confermare l'account.

## Passo 2: Caricare il codice su GitHub da VS Code

Visual Studio Code (VS Code) ha uno strumento integrato molto comodo per mandare il tuo codice direttamente su GitHub.

1. In VS Code, guarda la barra verticale all'estrema sinistra dello schermo. Clicca sull'icona che assomiglia a **tre pallini collegati da linee** (si chiama "Controllo del codice sorgente" o "Source Control").
2. Dovresti vedere un pulsante blu con scritto **"Publish to GitHub"** (Pubblica su GitHub). Cliccalo!
3. VS Code ti chiederà il permesso di collegarsi al tuo account GitHub. Clicca "Allow" (Consenti) e segui le istruzioni nel browser per autorizzarlo.
4. Una volta autorizzato, in alto al centro in VS Code apparirà un menu a tendina. Ti chiederà di scegliere il nome del repository (il "raccoglitore" del tuo progetto). Di default sarà `DND_Builder`.
5. Scegli l'opzione **"Publish to GitHub public repository"** (Pubblica come repository pubblico). *Scegliere "Pubblico" è importante affinché i tuoi amici e Streamlit possano vederlo.*
6. Aspetta qualche secondo: in basso a destra apparirà una notifica che dice "Successfully published...". Clicca su "Open on GitHub" se vuoi vedere il tuo codice online!

*Nota: Ogni volta che faremo delle modifiche al codice in futuro, dovrai tornare in quell'icona a sinistra (Source Control), scrivere un breve messaggio nella casella di testo (es. "Aggiunte razze"), cliccare sul pulsante "Commit" e poi su "Sync Changes" (Sincronizza modifiche) per mandare le novità su GitHub.*

## Passo 3: Mettere il sito online gratis con Streamlit Community Cloud

Ora che il tuo codice è su GitHub, possiamo trasformarlo in un sito web vero e proprio.

1. Vai su [Streamlit Community Cloud](https://share.streamlit.io/).
2. Clicca su **"Continue with GitHub"**. Questo collegherà Streamlit al tuo account GitHub.
3. Una volta dentro, clicca sul pulsante blu in alto a destra **"New app"** (Nuova app).
4. Se è la prima volta, potrebbe chiederti di autorizzare alcune cose, accetta.
5. Ti troverai in una pagina intitolata "Deploy an app". Compila i campi così:
   - **Repository**: Cerca e seleziona il tuo progetto (es. `tuo-nome-utente/DND_Builder`).
   - **Branch**: Lascia `main` (o `master`).
   - **Main file path**: Scrivi `app.py`.
   - **App URL**: Puoi scegliere un nome personalizzato per il link da dare ai tuoi amici (es. `dnd-tuonome.streamlit.app`).
6. Clicca sul pulsante **"Deploy!"** in basso.

Ci vorranno un paio di minuti, vedrai scorrere delle scritte (sta installando i programmi necessari) e poi... magia! Il tuo sito sarà online e pronto per essere usato. Puoi inviare il link dell'App URL al tuo gruppo di amici.

---
Se hai dubbi su qualsiasi passaggio, sono qui per aiutarti!