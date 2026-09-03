# Dev Container Dockerfile for m4.2_middleware_devinfra (step 0 bootstrap).
# Tool versions come from repo-root versions.env (via docker-compose.yml build args).
#
# Lean image: gh + OpenSpec (+ uv/Python) so this shared-infra repo is usable
# before issue #10 extracts the full product toolchain.

ARG DEVCONTAINER_BASE_IMAGE
FROM ${DEVCONTAINER_BASE_IMAGE}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG PYTHON_VERSION
ARG UV_VERSION
ARG STARSHIP_VERSION
ARG HADOLINT_VERSION
ARG YQ_VERSION
ARG NODE_VERSION
ARG OPENSPEC_VERSION

ENV DEBIAN_FRONTEND=noninteractive

# ── Base packages ─────────────────────────────────────────────────────────────
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    wget \
    gnupg \
    lsb-release \
    vim \
    git-lfs \
    jq \
    bash-completion \
    && git lfs install --system \
    && rm -rf /var/lib/apt/lists/*

# ── GitHub CLI (APT repos) ────────────────────────────────────────────────────
# hadolint ignore=DL3008
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
        | gpg --batch --yes --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
        > /etc/apt/sources.list.d/github-cli.list && \
    apt-get update && apt-get install -y --no-install-recommends \
        gh \
    && rm -rf /var/lib/apt/lists/*

# ── uv (Python package manager) ───────────────────────────────────────────────
RUN curl -fsSL "https://github.com/astral-sh/uv/releases/download/${UV_VERSION}/uv-x86_64-unknown-linux-gnu.tar.gz" \
        | tar -xz --strip-components=1 -C /usr/local/bin uv-x86_64-unknown-linux-gnu/uv uv-x86_64-unknown-linux-gnu/uvx

# ── yq ────────────────────────────────────────────────────────────────────────
RUN curl -fsSL "https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_linux_amd64" \
        -o /usr/local/bin/yq && chmod +x /usr/local/bin/yq

# ── hadolint ──────────────────────────────────────────────────────────────────
RUN curl -fsSL "https://github.com/hadolint/hadolint/releases/download/${HADOLINT_VERSION}/hadolint-Linux-x86_64" \
        -o /usr/local/bin/hadolint && chmod +x /usr/local/bin/hadolint

# ── Starship prompt ───────────────────────────────────────────────────────────
RUN curl -fsSL "https://github.com/starship/starship/releases/download/${STARSHIP_VERSION}/starship-x86_64-unknown-linux-gnu.tar.gz" \
        | tar -xz -C /usr/local/bin

# ── Node.js (official binary tarball; required by OpenSpec CLI) ───────────────
RUN curl -fsSL "https://nodejs.org/dist/${NODE_VERSION}/node-${NODE_VERSION}-linux-x64.tar.xz" \
        | tar -xJ --strip-components=1 -C /usr/local \
            "node-${NODE_VERSION}-linux-x64/bin" \
            "node-${NODE_VERSION}-linux-x64/include" \
            "node-${NODE_VERSION}-linux-x64/lib" \
            "node-${NODE_VERSION}-linux-x64/share" && \
    node --version && npm --version

# ── OpenSpec CLI (global install into /usr/local with system Node/npm) ────────
RUN npm install -g "@fission-ai/openspec@${OPENSPEC_VERSION}" && \
    openspec --version

# ── Bash completions (build-time, lazy-loaded via bash-completion) ───────────
RUN mkdir -p /usr/share/bash-completion/completions && \
    gh completion -s bash > /usr/share/bash-completion/completions/gh && \
    uv generate-shell-completion bash > /usr/share/bash-completion/completions/uv && \
    ln -sf /usr/share/bash-completion/completions/uv /usr/share/bash-completion/completions/uvx && \
    yq shell-completion bash > /usr/share/bash-completion/completions/yq && \
    starship completions bash > /usr/share/bash-completion/completions/starship

# ── Shell init (must run each session; not installable as static completions) ─
RUN echo 'eval "$(starship init bash)"' >> /etc/bash.bashrc

# ── Shell history persistence (volume-backed; filter agent/bootstrap noise) ──
# Cursor/VS Code agent shells dump dozens of `set +/-o …` lines into HISTFILE.
# With default HISTFILESIZE=500 those crowd out real commands after a restart.
# HISTIGNORE drops that noise; larger size + erasedups keep useful history.
RUN mkdir -p /commandhistory && \
    touch /commandhistory/.bash_history && \
    chown -R vscode /commandhistory && \
    cat >> /etc/bash.bashrc <<'EOF'
# Persistent bash history (/commandhistory volume)
export HISTFILE=/commandhistory/.bash_history
export HISTSIZE=100000
export HISTFILESIZE=100000
export HISTCONTROL=ignoreboth:erasedups
# Ignore IDE/agent shell-option bootstrap (set +/-o …) and trivial builtins
export HISTIGNORE='set *:unset *:shopt *:history *:exit:clear'
shopt -s histappend
# Append after each command so kill/rebuild does not lose the session
PROMPT_COMMAND="history -a${PROMPT_COMMAND:+; ${PROMPT_COMMAND}}"
EOF

# ── Switch to non-root user for uv tool installations
USER vscode

# ── Python (via uv; patch pin from versions.env → PYTHON_VERSION build-arg) ───
RUN uv python install "${PYTHON_VERSION}"
