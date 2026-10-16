---
layout: academic-publications
permalink: /publications/
title: Publications
description: Publications by Tao Hu and collaborators in world models, visual perception, and generative AI.
nav: false
nav_order: 2
---

<!-- _pages/publications.md -->

<!-- Bibsearch Feature -->

<label class="publication-search-label" for="bibsearch">Search publications</label>
{% include bib_search.liquid %}

<div class="publications">

<h2 class="bibliography">Preprints</h2>
{% bibliography --group_by none --group_order descending --query @*[booktitle=Arxiv] %}

{% bibliography --group_by year --group_order descending --query @*[booktitle!=Arxiv] %}

</div>
