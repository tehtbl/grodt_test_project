from whitenoise.storage import CompressedManifestStaticFilesStorage


class MyWhiteNoiseStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False
