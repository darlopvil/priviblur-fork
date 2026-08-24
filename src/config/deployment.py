from typing import NamedTuple, Optional


class DeploymentConfig(NamedTuple):
    """NamedTuple that stores configuration values relating to deployment

    Attributes:
        host: Host to bind to.
        port: Port to listen for connections.
        domain: Hostname under which this instance is hosted, WITHOUT a scheme
            (example.com, not https://example.com).

            It is used for two things that need different formats: as the
            Domain attribute of the settings cookie, which must be a bare
            hostname, and as the prefix of absolute URLs, which needs a scheme.
            Storing the hostname and deriving the URL from `https` keeps a
            single option that is valid for both. See issue #19.

        https: Enables secure cookies and forces all links to priviblur to use the `https://` scheme

        workers: Amount of worker Priviblur instances to spawn.
            Increases speed significantly
    """

    host: str = "127.0.0.1"
    port: int = 8080
    domain: Optional[str] = None

    https: bool = False

    workers: int = 1

    @property
    def base_url(self) -> str:
        """Absolute URL of this instance, or an empty string when unset.

        Empty means callers fall back to relative URLs, which work fine for
        browsing and are only a problem for feeds consumed elsewhere.
        """
        if not self.domain:
            return ""

        scheme = "https" if self.https else "http"
        return f"{scheme}://{self.domain}"