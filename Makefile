## help: muestra este mensaje de ayuda
.PHONY: help
help:
	@echo 'Usage:'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'

## install: instala las dependencias necesarias
.PHONY: install
install:
	pip install --requirement requirements.txt

## fmt: formatea todo el contenido del libro y código
.PHONY: fmt
fmt:
	mdformat --number contenidos/**/*.md
	black --line-length 120 .

## build: compila el libro ejecutando las celdas
.PHONY: build
build:
	cd contenidos && myst build --execute

## clean: elimina todos los archivos generados por la compilación
.PHONY: clean
clean:
	cd contenidos && myst clean --all --yes

## start: inicia el servidor de desarrollo ejecutando las celdas
.PHONY: start
start:
	cd contenidos && myst start --execute
