"""Builds a GeneList file upon request.
"""

from flask import Blueprint, Response

from g2e.db import dataaccess
from g2e.config import Config
from g2e.core.genelist import filemaker

genelist_api = Blueprint('genelist', __name__, url_prefix=Config.BASE_URL + '/genelist')


@genelist_api.route('/<direction>/<extraction_id>')
def get_genelist(direction, extraction_id):
    """Handle GET request based on extraction ID.
    """
    gene_signature = dataaccess.fetch_gene_signature(extraction_id)
    genelist = __get_genelist_by_direction(gene_signature, int(direction))
    genelist_str = filemaker.get_file_contents_as_string(genelist)
    response = Response(genelist_str, mimetype='text/plain')
    return response


def __get_genelist_by_direction(gene_signature, direction):
    for gene_list in gene_signature.gene_lists:
        if gene_list.direction == direction:
            return gene_list
    return None