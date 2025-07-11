import os
import random
import re
import sys

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
    total_pages = len(corpus)
    probablities = dict()
    links = corpus[page]
    if len(links) == 0:
        for p in corpus:
            probablities[p] = 1/total_pages
        return probablities
    for p in corpus:
        probablities[p] = (1-damping_factor)/total_pages
        if p in links:
            probablities[p] += damping_factor/len(links)
    return probablities

def weighted_choice(pages, probs):
    r = random.uniform(0,1)
    cumlative = 0.0
    for page, prob in zip(pages, probs):
        cumlative += prob
        if r < cumlative:
            return page #manually implemented random choices for the argument 'weights' [nevermind, I didn't save the file;(]

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_counts = {page:0 for page in corpus}

    page = random.choice(list(corpus.keys()))
    for _ in range(n):
        page_counts[page] += 1
        model= transition_model(corpus, page, damping_factor)

        pages = list(model.keys())
        probs = list(model.values())
        page = weighted_choice(pages, probs)
    pagerank = {page:count / n for page, count in page_counts.items()}
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)
    pagerank = {page:1/n for page in corpus}
    converged = False
    while not converged:
        new_pagerank = {}
        for page in corpus:
            rank = (1-damping_factor)/n
            for potential_linker in corpus:
                if corpus[potential_linker]:
                    if page in corpus[potential_linker]:
                        rank += damping_factor * (pagerank[potential_linker]/len(corpus[potential_linker]))
                else:
                    rank += damping_factor * (pagerank[potential_linker]/n)
            new_pagerank[page] = rank
        converged = all(abs(new_pagerank[page]-pagerank[page]) < 0.001 for page in corpus)
        pagerank = new_pagerank
    return pagerank


if __name__ == "__main__":
    main()
