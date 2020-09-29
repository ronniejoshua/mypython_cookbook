#! /usr/bin/env python3

import pandas as pd
import uuid
import random
import string
import numpy as np
import logging
import mylogging.webvisit_generator

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s - %(module)s - %(funcName)s'
formatter = logging.Formatter(FORMAT, datefmt='%d-%b-%y %H:%M:%S')

file_handler = logging.FileHandler('data_generator.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)


logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def generate_medium_authors_table(n: int) -> pd.DataFrame:
    """
    Generate Medium authors table (using randomly generated data).

    Output is saved as a .csv file

    :param n: Number of entries.
    :return: A pandas dataframe with medium author data.
    """

    df_dict = {
        "author_id": [str(uuid.uuid4()) for i in range(n)],
        "author_first_name": [
            "".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(5, 10))) for i in range(n)
        ],
        "author_last_name": [
            "".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(3, 10))) for i in range(n)
        ],
    }

    df_dict["email"] = [
        f"{first_name}.{last_name}@mymail.com"
        for first_name, last_name in zip(df_dict["author_first_name"], df_dict["author_last_name"])
    ]

    df = pd.DataFrame(df_dict)
    df.to_csv("medium_authors_table.csv", index=False)
    return df


def generate_medium_posts_table(authors_df: pd.DataFrame) -> None:
    """
    Generate a table with Medium posts entries.

    :param authors_df: The authors data.
    """

    entries: dict = {
        "post_id": [],
        "author_id": [],
        "article_title": [],
    }

    for idx, row in authors_df.iterrows():
        n_posts = random.randint(0, 100)
        entries["post_id"] += [str(uuid.uuid4()) for i in range(n_posts)]
        entries["author_id"] += [row["author_id"]] * n_posts
        entries["article_title"] += [
            "".join(np.random.choice([i for i in string.ascii_lowercase], random.randint(10, 30)))
            for i in range(n_posts)
        ]

    df = pd.DataFrame(entries)
    df.to_csv("medium_posts_table.csv", index=False)


if __name__ == "__main__":
    logger.debug("Starting data generation")
    # df = generate_medium_authors_table(n=100)
    # generate_medium_posts_table(authors_df=df)
    logger.info("Ending data generation")

