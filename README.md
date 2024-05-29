# Extend Codegen CLI

A tool for generating an AccelByte SDK module or plugin for custom services,
such as services created using Extend Service Extension.

:exclamation: **This repository contains the codegen template pack zip 
releases only.**

## Overview

The Extend Codegen consists of a CLI app and some template packs. The CLI app is
released as container images in 
[Docker Hub](https://hub.docker.com/r/accelbyte/extend-codegen-cli) while 
the template pack zip files are released 
[here](https://github.com/AccelByte/extend-codegen-cli/releases) 
in this repository.

A template pack contains a `Makefile` and `Jinja` template files. When the
`Makefile` command is invoked, the Extend Codegen CLI app is executed with the
`Jinja` template files and a given custom service OpenAPI 2.0 JSON file to 
generate code. The `Makefile` also fetches the specified CLI container image
version if it is not available locally yet.

## General Usage

1. Download the template pack zip for the corresponding AccelByte SDK module or
plugin [here](https://github.com/AccelByte/extend-codegen-cli/releases) 

2. Unzip the downloaded template pack zip file and follow the instruction in 
the README.md inside.

   