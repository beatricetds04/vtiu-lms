"""LiveKit access-token helpers."""


def build_livekit_token(api_key, api_secret, room_name, identity, display_name, role):
    """Build a short-lived token for a LiveKit room participant.

    Accepts either the canonical role string used by the web app
    (publisher/audience) or the legacy boolean publisher flag used by the
    mobile API compatibility helper.
    """
    if not api_key or not api_secret:
        raise RuntimeError(
            'LIVEKIT_API_KEY and LIVEKIT_API_SECRET must both be configured.'
        )

    try:
        from importlib import import_module

        api = import_module('livekit.api')
    except ImportError as exc:
        raise RuntimeError(
            'The LiveKit server SDK is not installed.'
        ) from exc

    # Normalize the role signal across the two contracts.
    if role is True or role == 'publisher':
        can_publish = True
    elif role is False or role == 'audience':
        can_publish = False
    else:
        raise ValueError("LiveKit role must be 'publisher' or 'audience'.")

    try:
        grants = api.VideoGrants(
            room_join=True,
            room=room_name,
            can_publish=can_publish,
            can_subscribe=True,
        )
        return (
            api.AccessToken(api_key, api_secret)
            .with_identity(str(identity))
            .with_name(display_name or str(identity))
            .with_grants(grants)
            .to_jwt()
        )
    except Exception as exc:
        raise RuntimeError(
            'LiveKit token generation failed. Verify the configured API key and secret belong to the same LiveKit project.'
        ) from exc
