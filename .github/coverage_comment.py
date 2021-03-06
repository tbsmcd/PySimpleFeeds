import os


def create_comment():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cov_file = base_dir + '/cov.txt'
    with open(cov_file) as f:
        lines = f.readlines()
        coverage = ''
        for line in lines:
            line = line.strip()
            if line.startswith('TOTAL ') and line.endswith('%'):
                coverage = line
        coverage = coverage.split()[3]
        txt = ''.join(lines)
        comment = """
<img src="https://img.shields.io/badge/pytest-passing-9ACD32.svg" alt="pytest passing"> <img src="https://img.shields.io/badge/coverage-{cov}2525-6A5ACD.svg" alt="coverage">
<details>
<pre>
<code>
{txt}
</code>
</pre>
</details> 
        """.format(cov=coverage, txt=txt)\
            .replace('-----------', '___________').replace('------', '')\
            .replace('_________________________________', ' ')
        print(comment)


if __name__ == '__main__':
    create_comment()
