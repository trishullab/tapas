def finalize(config):
    fs = config.target.fs
    fs.protocol if isinstance(fs.protocol, str) else fs.protocol[0]