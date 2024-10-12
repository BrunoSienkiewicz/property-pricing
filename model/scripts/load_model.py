import argparse
from artifacts_handler import ArtifactHandler, LocalArtifactHandler, DBArtifactHandler, S3ArtifactHandler

def load_model(model_name: str, model_version: str, artifacts_handler: ArtifactHandler, from_uri: str, to_uri: str):
    model, config, ohe_encoder, ordinal_encoder, scaler = artifacts_handler.load_model(model_name, model_version, from_uri)
    artifacts_handler.save_model(model, config, ohe_encoder, ordinal_encoder, scaler, model_name, model_version, to_uri)
    return model, config, ohe_encoder, ordinal_encoder, scaler


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--model_version", type=str, required=True)
    parser.add_argument("--load_from", type=str, required=True, choices=["db", "dir", "s3"])
    parser.add_argument("--from_uri", type=str, required=True)
    parser.add_argument("--load_to", type=str, required=True, choices=["db", "dir", "s3"])
    parser.add_argument("--to_uri", type=str, required=True)
    args = parser.parse_args()

    if args.load_from == "db":
        artifacts_handler = DBArtifactHandler
    elif args.load_from == "dir":
        artifacts_handler = LocalArtifactHandler
    elif args.load_from == "s3":
        artifacts_handler = S3ArtifactHandler
    else:
        raise ValueError("load_from must be one of 'db', 'dir', 's3'")

    if args.load_to == "db":
        artifacts_handler = DBArtifactHandler
    elif args.load_to == "dir":
        artifacts_handler = LocalArtifactHandler
    elif args.load_to == "s3":
        artifacts_handler = S3ArtifactHandler
    else:
        raise ValueError("load_to must be one of 'db', 'dir', 's3'")

    load_model(args.model_name, args.model_version, artifacts_handler, args.from_uri, args.to_uri)


