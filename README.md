# Check certs

Very simple python cli app to check Let's encrypt certificats status on a nginx-proxy docker instance.

## How-To

In your docker server, you can execute cli app using this command line:

```bash
docker run --rm -it -v <local directory with your cert files>:/certs  ghcr.io/lpoaura/check_le_certs:latest
```

You can get output as json using `--json`

To filter output by status (`valid`, `expiring`, `expired`), you can use cli argument `--category {all,valid,expiring,expired}`


## License

This plugin is licenced with[GNU General Public License, version 3](https://www.gnu.org/licenses/gpl-3.0.html)


See [LICENSE](LICENSE) for more information.

## Tooling

This project is configured with the following tools:

- [Black](https://black.readthedocs.io/en/stable/) to format the code without any existential question
- [iSort](https://pycqa.github.io/isort/) to sort the Python imports

Code rules are enforced with [pre-commit](https://pre-commit.com/) hooks.  
Static code analisis is based on: both

See also: [contribution guidelines](CONTRIBUTING.md).

## Documentation

The documentation is generated using Sphinx and is automatically generated through the CI and published on Pages.

- homepage: <https://github.com/lpoaura/check_le_certs>
- repository: <https://github.com/lpoaura/check_le_certs>
- tracker: <https://github.com/lpoaura/check_le_certs/issues>

# Contributors

<a href="https://github.com/lpoaura/check_le_certs/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=lpoaura/check_le_certs" />
</a>


<img align="center" src="https://github.com/lpoaura/PluginQGis-LPOData/blob/master/plugin_qgis_lpo/resources/images/logo_lpo_aura.png">