# =============================================================================
# claude-meta-autoagent — DevContainer
# =============================================================================
# General-purpose Claude Code development container.
#
# Runtime isolation (Claude Code infra != project code):
#   Claude Code — native binary (~/.local/bin/claude, auto-updated)
#   Node.js     — system Node 22 LTS (devcontainers/cli, general use)
#   Python      — system python3 + uv (general-purpose package manager)
#   Project Node.js can be added via PROJECT_NODE_VERSION build arg
# =============================================================================
FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

ARG PROJECT_NODE_VERSION=
ARG USERNAME=vscode
ARG DOCKER_GID=999

# UTF-8 encoding and timezone
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    TZ=UTC \
    DEVCONTAINER=true

# =============================================================================
# Layer 1: System packages (root)
# =============================================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales tzdata \
    && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen en_US.UTF-8 \
    && ln -snf /usr/share/zoneinfo/UTC /etc/localtime \
    && echo "UTC" > /etc/timezone \
    && apt-get install -y --no-install-recommends \
    build-essential git git-lfs curl wget less procps sudo ca-certificates gnupg2 openssh-client \
    ripgrep fd-find fzf tree htop vim nano zsh tmux jq unzip zip man-db gh \
    python3 python3-pip python3-venv \
    docker.io \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    # Node.js LTS
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g @devcontainers/cli \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && (groupmod -g ${DOCKER_GID} docker 2>/dev/null || groupadd -g ${DOCKER_GID} docker 2>/dev/null || true) \
    && usermod -aG docker ${USERNAME} \
    # Docker Compose v2 plugin
    && mkdir -p /usr/local/lib/docker/cli-plugins \
    && curl -SL "https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-$(uname -m)" -o /usr/local/lib/docker/cli-plugins/docker-compose \
    && chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# =============================================================================
# Layer 2: User setup (root -> vscode)
# =============================================================================
RUN echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN mkdir -p /commandhistory /workspaces \
    && touch /commandhistory/.bash_history \
    && chown -R ${USERNAME}:${USERNAME} /commandhistory /workspaces

USER ${USERNAME}

# PATH: include static paths so Claude Code + uv are always resolved
ENV HOME=/home/${USERNAME} \
    NVM_DIR=/home/${USERNAME}/.nvm \
    PATH=/home/${USERNAME}/.local/bin:${PATH}

# =============================================================================
# Layer 3: Claude Code CLI — Native Installer
# OOM prevention: run from temp directory
# =============================================================================
RUN mkdir /tmp/claude-install && cd /tmp/claude-install \
    && curl -fsSL https://claude.ai/install.sh | bash \
    && rm -rf /tmp/claude-install \
    && cd ~ \
    && claude --version

# =============================================================================
# Layer 4: Node.js — Project (optional)
# Separate from system Node.js (Layer 1). Installed only when PROJECT_NODE_VERSION is set.
# =============================================================================
RUN if [ -n "${PROJECT_NODE_VERSION}" ]; then \
        mkdir -p ${NVM_DIR} \
        && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash \
        && . ${NVM_DIR}/nvm.sh \
        && nvm install ${PROJECT_NODE_VERSION} \
        && nvm alias project-node ${PROJECT_NODE_VERSION} \
        && nvm alias default ${PROJECT_NODE_VERSION}; \
    fi

# =============================================================================
# Layer 5: uv (Python package manager)
# =============================================================================
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# =============================================================================
# Layer 6: User settings (shell, editor, git)
# =============================================================================
RUN mkdir -p ${HOME}/.claude ${HOME}/.config/nano

# .bashrc
RUN echo 'export LANG=en_US.UTF-8' >> ${HOME}/.bashrc \
    && echo 'export LC_ALL=en_US.UTF-8' >> ${HOME}/.bashrc \
    && echo 'export HISTFILE=/commandhistory/.bash_history' >> ${HOME}/.bashrc \
    && echo 'export HISTSIZE=10000' >> ${HOME}/.bashrc \
    && echo 'export HISTFILESIZE=20000' >> ${HOME}/.bashrc \
    && echo 'export NVM_DIR="${HOME}/.nvm"' >> ${HOME}/.bashrc \
    && echo '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"' >> ${HOME}/.bashrc \
    && echo 'if command -v nvm &>/dev/null; then if [ -f ".nvmrc" ]; then nvm use 2>/dev/null || true; else nvm use project-node 2>/dev/null || true; fi; fi' >> ${HOME}/.bashrc \
    && echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> ${HOME}/.bashrc \
    && echo 'alias ll="ls -alF"' >> ${HOME}/.bashrc \
    && echo 'alias fd="fdfind"' >> ${HOME}/.bashrc

# Vim
RUN echo 'set encoding=utf-8' >> ${HOME}/.vimrc \
    && echo 'set fileencoding=utf-8' >> ${HOME}/.vimrc \
    && echo 'set termencoding=utf-8' >> ${HOME}/.vimrc \
    && echo 'set number' >> ${HOME}/.vimrc \
    && echo 'set tabstop=4' >> ${HOME}/.vimrc \
    && echo 'set shiftwidth=4' >> ${HOME}/.vimrc \
    && echo 'set expandtab' >> ${HOME}/.vimrc

# Nano
RUN echo 'set tabsize 4' >> ${HOME}/.nanorc \
    && echo 'set tabstospaces' >> ${HOME}/.nanorc \
    && echo 'set linenumbers' >> ${HOME}/.nanorc

# Git (UTF-8)
RUN git config --global core.quotepath false \
    && git config --global i18n.commitEncoding utf-8 \
    && git config --global i18n.logOutputEncoding utf-8

# =============================================================================
# Setup scripts + Entrypoint
# =============================================================================
USER root
COPY setup-env.sh /usr/local/bin/
COPY entrypoint.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/setup-env.sh /usr/local/bin/entrypoint.sh

USER ${USERNAME}
WORKDIR /workspaces

# ENTRYPOINT: always runs on container start
# -> auto-runs setup-env.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["sleep", "infinity"]
