#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    # Generate a human-readable timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    run = wandb.init(job_type="basic_cleaning", name=f"Run_{timestamp}")
    run.config.update(args)

    local_path = wandb.use_artifact("sample.csv:latest").file()
    df = pd.read_csv(local_path)
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    df.to_csv(args.output_artifact, index=False)
    #upload dataframe df as a new wandb artifact 
    artifact = wandb.Artifact(args.output_artifact, type=args.output_type, description=args.output_description)
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)
    artifact.wait()
    
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help='input artifact name',
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help='output artifact name',
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help='type of output artifact',
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help='description of output artifact',
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help='minimum price filter',
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help='maximum price filter',
        required=True
    )


    args = parser.parse_args()

    go(args)
