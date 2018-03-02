"""
Table Binned Heatmap
-----------------------
This example shows how to make a heatmap.
"""

import altair as alt
from vega_datasets import data

source = data.movies.url

chart = alt.Chart(source).mark_rect().encode(
    x = alt.X('IMDB_Rating:Q', bin = alt.BinParams(maxbins=60)), 
    y = alt.Y('Rotten_Tomatoes_Rating:Q', bin = alt.BinParams(maxbins=40)),
    color = alt.Color('count(IMDB_Rating):Q',
                      scale=alt.Scale(scheme='greenblue'))
)