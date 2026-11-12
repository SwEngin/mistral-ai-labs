FROM python:3.12-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl git unzip

ENV MISTRAL_INSTALL_BUN=1 \
    MISTRAL_NO_MODIFY_PATH=1 \
    PATH="/root/.mistral/bin:/root/.bun/bin:/usr/local/bin:${PATH}"

RUN curl -fsSL https://mistral.ai/cli/install.sh -o /tmp/mistral-install.sh \
    && bash /tmp/mistral-install.sh \
    && rm /tmp/mistral-install.sh \
    && python -m pip install --no-cache-dir "uv>=0.9,<1" \
    && mistral --version \
    && bun --version \
    && uv --version

WORKDIR /workspace
CMD ["bash"]
