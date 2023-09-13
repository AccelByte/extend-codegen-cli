DOCKER_TAG_VERSION := latest
DOCKER_TAG := accelbyte/codegen:$(DOCKER_TAG_VERSION)

EXE_VERSION := v0.0.2
EXE_FLAVOR := linux_amd64
EXE_URL := https://github.com/AccelByte/extend-codegen-cli/releases/download/$(EXE_VERSION)/accelbyte-codegen-$(EXE_FLAVOR)

download:
	wget $(EXE_URL) -O accelbyte-codegen

build: accelbyte-codegen
	docker build --tag $(DOCKER_TAG) .
