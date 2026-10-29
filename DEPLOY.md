# Deployment

Pushes to `main` that pass CI are built into a Docker image, pushed to GitHub
Container Registry, and deployed to Render (`.github/workflows/deploy.yml`).

```
push to main → CI (tests + docker build) → push ghcr.io/<owner>/<repo>:<sha> → Render deploy hook
```

## One-time setup

1. **Image visibility.** After the first run, open the package under the
   repository's *Packages* and set it to **Public** (or give Render a registry
   credential for GHCR, see below).
2. **Render service.** In Render choose *New → Web Service → Existing image* and
   use `ghcr.io/<owner>/<repo>:latest` (owner and repo in lowercase). Pick the
   free instance type.
3. **Environment variable.** On the Render service set `DATABASE_URL`
   (`app.py` reads it at import time and fails without it).
4. **Deploy hook.** In the Render service go to *Settings → Deploy Hook*, copy
   the URL, and add it to this repository as an Actions secret named
   `RENDER_DEPLOY_HOOK` (*Settings → Secrets and variables → Actions*).
5. If the image stays private, add a GHCR credential in Render
   (*Account Settings → Registry Credentials*) using a GitHub personal access
   token with the `read:packages` scope.

Until `RENDER_DEPLOY_HOOK` is set, the workflow still pushes the image and
logs a warning instead of deploying.
