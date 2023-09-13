# Running `accelbyte-codegen` inside a container

Use the following command to download the executable.

```shell
make download EXE_VERSION=0.1.0
```

Use the following command to create the image.

```shell
make build
```

Use the following command to run the executable. 

```shell
docker run --rm --tty accelbyte-codegen --help
```
