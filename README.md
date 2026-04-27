# Distributed Text Services Registry

A central registry of API instances that implement the
[Distributed Text Services (DTS)](https://dtsapi.org/) specification.

The registry allows interoperable clients and aggregators to easily discover
DTS-compliant APIs. For API publishers, this broadens the published material's
audience and makes it more accessible. For those developing client software, it
furnishes access points for a wide variety of diverse corpora.

The registry is published as a single
[JSON-LD](https://www.w3.org/TR/json-ld11/) document,
[`registry.json`](./registry.json), modelled as a
[DCAT](https://www.w3.org/TR/vocab-dcat-3/) Catalog of `dcat:DataService`s, and
validated against [`registry.schema.json`](./registry.schema.json) (JSON Schema
2020-12).

## Adding or updating an entry

To add your API entry point to the registry, first make a fork of this
dts-registry repository that you can freely edit. Then

1. In your fork, **append a new object** to the `entries` array of
   [`registry.json`](./registry.json) using the structure above.
2. Validate the file (see below). It MUST be valid JSON and SHOULD validate
   against [`registry.schema.json`](./registry.schema.json).
3. Open a pull request.

The full shape of the entry objects is described below. Note that

- the public URL of the API's Entry endpoint should be used both as the entry's
  `@id` and as its `endpointURL`.
- The `dtsVersion` and `status` MUST be chosen from the tables of allowed values
  below.

## Document shape

The registry document is a `dcat:Catalog`. Each entry is a `dcat:DataService`
identified by the URL of its DTS Entry Endpoint.

```json
{
  "@context": [
    "https://dtsapi.org/context/v1.0.json",
    { "...": "dcat: + registry-local terms" }
  ],
  "@id": "https://distributed-text-services.github.io/dts-registry/",
  "@type": "Catalog",
  "title": "DTS Registry",
  "description": "...",
  "entries": [
    {
      "@id": "https://example.org/api/dts",
      "@type": "DataService",
      "title": "Example DTS API",
      "description": "Optional human-readable description of the corpus and API.",
      "dtsVersion": "1.0",
      "status": "production",
      "endpointURL": "https://example.org/api/dts",
      "contactPoint": [
        {
          "@type": "Individual",
          "fullName": "Example Maintainer",
          "email": "mailto:maintainer@example.org"
        }
      ]
    }
  ]
}
```

## Allowed `dtsVersion` strings

The `dtsVersion` of each entry MUST be the official version identifier of a
published DTS version. The strings "pre-alpha" and "unknown" are reserved for
earlier unofficial releases and for APIs which do not publish any version
information.

| Value       | Spec page                                                                                             |
| ----------- | ----------------------------------------------------------------------------------------------------- |
| `1.0`       | <https://dtsapi.org/versions/v1.0>                                                                    |
| `1.0rc1`    | <https://distributed-text-services.github.io/specifications/versions/1.0rc1/>                         |
| `1-alpha`   | <https://distributed-text-services.github.io/specifications/versions/1-alpha/>                        |
| `1-draft`   | [`1-draft2`](https://github.com/distributed-text-services/specifications/tree/main/versions/1-draft2) |
| `pre-alpha` | (no published spec)                                                                                   |
| `unknown`   | (no published spec)                                                                                   |

## Allowed `status` values

The `status` of each entry MUST be exactly one of:

| Value          | Meaning                                                                                                                                                              |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `production`   | A stable, actively maintained service intended for real-world use.                                                                                                   |
| `development`  | A service intended for production but currently incomplete or pre-release. Distinct from `experimental` in that the maintainers' goal is a production-grade service. |
| `demo`         | A publicly accessible demonstration; data and availability may be unstable.                                                                                          |
| `experimental` | A research-oriented API which may not be intended for eventual production use; availability and conformance are not guaranteed.                                      |
| `deprecated`   | A previously listed instance that is no longer maintained or recommended.                                                                                            |

## Validating your addition

This project uses [`uv`](https://docs.astral.sh/uv/) and Python 3.14. The Python
version is pinned in [`.python-version`](./.python-version) and dependencies are
declared in [`pyproject.toml`](./pyproject.toml) with a resolved
[`uv.lock`](./uv.lock).

To set up the environment and validate the registry, first ensure that `uv` is
installed locally. Then run:

```bash
uv sync
uv run scripts/validate.py
```

`uv sync` will, on first run, download Python 3.14 if it isn't already
installed, create a `.venv/`, and install the dev dependencies (currently just
`jsonschema`). `uv run scripts/validate.py` parses
[`registry.json`](./registry.json), checks the schema document itself, and
validates the registry against it, printing the failing JSON pointer for each
error.
