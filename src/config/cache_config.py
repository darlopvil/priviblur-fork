from typing import NamedTuple, Optional


class CacheConfig(NamedTuple):
    """NamedTuple that stores configuration values relating to the cache

    Attributes:
        url: to connect to the Valkey (or Redis) instance. Both speak the same
            protocol and use the redis:// scheme.

        connect_timeout: Seconds to wait when opening the connection to the
            cache. Deliberately short: this is a local cache, and while it is
            down every request pays this wait before falling back. See #21.

        socket_timeout: Seconds to wait for a reply once connected.
        cache_active_poll_results_for: Amount of seconds to cache poll results from active polls
        cache_expired_poll_results_for: Amount of seconds to cache poll results from expired polls
    """

    url: Optional[str] = None

    connect_timeout: int = 1
    socket_timeout: int = 2

    cache_active_poll_results_for: int = 3600
    cache_expired_poll_results_for: int = 86400
    cache_feed_for: int = 3600
    cache_blog_feed_for: int = 3600
    cache_blog_post_for: int = 300
