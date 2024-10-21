import os
import random
import re
import sys
from collections import defaultdict

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    result = {}
    N = len(corpus)
    if page not in corpus:
        return result

    # initial probability for every page
    for p in corpus:
        result[p] = (1 - damping_factor) / N
    
    # Add probability to all the links in the page
    numlink = len(corpus[page])
    for p in corpus[page]:
        result[p] = result[p] + damping_factor / numlink

    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    visited = {page: 0 for page in pages}
    models = {}

    for page in pages:
        models[page] = transition_model(corpus=corpus, page=page, damping_factor=damping_factor)
    
    # Get the first sample
    next_sample = random.choice(pages)
    visited[next_sample] += 1
    count = n
    while count - 1 > 0:
        next_model = models[next_sample]
        # Get next sample
        next_sample = generate_next_sample(next_model)
        count -= 1
        # Record visited page
        visited[next_sample] += 1
    
    # Return estimated page rank
    return {page : visited[page] / n for page in visited}


def generate_next_sample(model):
    """
    Return the next sample base on the probability in the model
    """
    pages = []
    counts = []
    for page, count in model.items():
        pages.append(page)
        counts.append(int(count * 1000))
    
    return random.sample(pages, counts=counts, k=1)[0]


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    N = len(pages)
    # Initial the same page rank for each page
    pageranks = {page: 1 / N for page in pages}

    # Build the backlinks for later calculation
    backlinks = defaultdict(set)
    for page in pages:
        for source, targets in corpus.items():
            # Assume page without any link can visit all N pages
            if not targets or page in targets:
                backlinks[page].add(source)
    
    # Iterate the page rank algorithm until every page's page rank change less than 0.001
    converge = False
    while not converge:
        new_pageranks = defaultdict(float)
        # Recalculate each page's page rank
        for page in pages:
            new_pageranks[page] = (1 - damping_factor) / N
            sigma = 0
            for link in backlinks.get(page, []):
                # If the source page has no link, assume it can visit all N pages.
                numLinks = N if not corpus[link] else len(corpus[link])
                sigma += pageranks[link] / numLinks
            new_pageranks[page] += damping_factor * sigma
    
        # Normalise the new pageranks
        # norm_factor = sum(new_pageranks.values())
        # new_pageranks = {page: (rank / norm_factor) for page, rank in new_pageranks.items()}

        # Evaluate if the new_pageranks converge with previous pageranks
        converge = all(abs(new_pageranks[page] - pageranks[page]) <= 0.001 for page in pages)

        # Assign new_pageranks to pageranks
        pageranks = new_pageranks

    return pageranks


if __name__ == "__main__":
    main()
