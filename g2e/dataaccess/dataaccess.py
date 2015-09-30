"""Handles all database transactions. It has knowledge of the primary classes
and their relationships and saves them accordingly.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import sqlalchemy as sa

from g2e.dataaccess.util import session_scope
from g2e.model.genelist import GeneList
from g2e.model.genesignature import GeneSignature
from g2e.model.softfile import SoftFile
from g2e.model.tag import Tag
from g2e.model.optionalmetadata import OptionalMetadata


def fetch_all(klass):
    """Fetches all entities of a specific class.
    """
    with session_scope() as session:
        return session.query(klass).all()


def save_gene_signature(gene_signature):
    """Saves the SoftFile and GeneList to the database and returns the ID from
    the extraction table.
    """
    with session_scope() as session:
        session.add(gene_signature)
        session.commit()
        return gene_signature.extraction_id


def fetch_gene_signature(extraction_id):
    """Single entry point for fetching extractions from database by ID.
    """
    with session_scope() as session:
        return session\
            .query(GeneSignature)\
            .filter(GeneSignature.extraction_id == extraction_id)\
            .first()


def fetch_tag(tag_name):
    """Fetches tags based on name.
    """
    with session_scope() as session:
        return session\
            .query(Tag)\
            .filter(Tag.name == tag_name)\
            .first()


def fetch_metadata(metadata_name):
    """Fetches metadata based on name.
    """
    with session_scope() as session:
        return session\
            .query(OptionalMetadata)\
            .filter(OptionalMetadata.name == metadata_name)\
            .all()


def fetch_metadata_by_value(metadata_name, metadata_value):
    """Fetches metadata based on name and value.
    """
    with session_scope() as session:
        return session\
            .query(OptionalMetadata)\
            .filter(OptionalMetadata.name == metadata_name)\
            .filter(OptionalMetadata.value == metadata_value)\
            .all()


def get_statistics():
    """Returns hash with DB statistics for about page.
    """
    with session_scope() as session:
        num_gene_signatures = session.query(GeneSignature).count()
        num_gene_lists = session.query(GeneList).count()
        num_tags = session.query(Tag).count()
        platforms = session.query(sa.func.distinct(SoftFile.platform))

    platform_counts = {}
    num_platforms = platforms.count()
    for platform in platforms:
        platform = platform[0]
        count = session.query(GeneSignature, SoftFile)\
            .filter(SoftFile.gene_signature_fk == GeneSignature.id)\
            .filter(SoftFile.platform == platform)\
            .count()
        platform_counts[platform] = count

    return {
        'num_gene_signatures': num_gene_signatures,
        'num_gene_lists': num_gene_lists,
        'num_tags': num_tags,
        'num_platforms': num_platforms,
        'platform_counts': platform_counts
    }