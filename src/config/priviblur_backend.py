from typing import NamedTuple, Optional


class PriviblurBackendConfig(NamedTuple):
    """NamedTuple that stores configuration values relating to Priviblur Extractor

    Attributes:
        main_response_timeout: Total timeout for API requests to Tumblr
        image_response_timeout: Total timeout for media requests to Tumblr

        main_connect_timeout: Timeout for establishing the connection on API
            requests. Unset means no specific limit.
        main_read_timeout: Timeout between two chunks of data on API requests.
            Unset means no specific limit.

        image_connect_timeout: As above, for media requests.
        image_read_timeout: As above, for media requests.

        authorization_token: Overrides the bearer token sent to Tumblr's API.
            Unset means using TumblrAPI.DEFAULT_AUTHORIZATION_TOKEN.

        allow_external_embeds: Renders embedded players (YouTube, Spotify,
            Vimeo...) as real iframes instead of a link card.

            Off by default and it should stay off on public instances: an
            iframe loads straight from the third party in the visitor's
            browser, bypassing the proxy entirely. The provider then sees the
            real IP, the real user agent, and can set cookies, which defeats
            the whole point of running this. See issue #23.

    The total timeout covers the whole operation. Splitting it lets a slow but
    working response finish while still failing fast on an unreachable host.
    """

    main_response_timeout: int = 10
    image_response_timeout: int = 30

    main_connect_timeout: Optional[int] = None
    main_read_timeout: Optional[int] = None

    image_connect_timeout: Optional[int] = None
    image_read_timeout: Optional[int] = None

    authorization_token: Optional[str] = None

    allow_external_embeds: bool = False