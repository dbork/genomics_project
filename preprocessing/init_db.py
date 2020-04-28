import os
import sqlite3

# Helper function for obtaining short column names from file subpaths
def subpath_to_colname(subdir, filename):
    return '{}_{}_{}'.format(
        subdir, 
        filename.split('_')[1],
        filename.split('_')[0]
    )

# Store directory structure in memory
pathbase = '/home/dbork/genomics/data'
subdirs = os.listdir(pathbase)
filenames = {subdir: [] for subdir in subdirs}
for subdir in subdirs:
    if subdir == 'README.txt':
        continue
    for filename in os.listdir('{}/{}'.format(pathbase, subdir)):
        if filename[0] == '.':
            continue
        filenames[subdir].append(filename)

# First, initialize the table in sqlite
cols = []
for subdir in subdirs:
    for filename in filenames[subdir]:
        cols.append(subpath_to_colname(subdir, filename))

conn = sqlite3.connect('../data/rpkm.db')
c = conn.cursor()

init_query = '''CREATE TABLE rpkm (
                gene TEXT,
                {} REAL
            )'''.format(' REAL, '.join(cols))
print init_query
c.execute(init_query)

# Next, loop over all raw data files to obtain gene expression data. This is
# fairly memory-intensive, but the alternative is very slow due to needing to
# execute many UPDATE queries.

genes = []
data = {}

for subdir in subdirs:
    print 'Adding gene names from dataset {}...'.format(subdir)
    count = 0
    for filename in filenames[subdir]:
        count += 1
        print filename
        geneset = set(genes)
        newgenes = 0

        f = open('{}/{}/{}'.format(pathbase, subdir, filename))
        for line in f.readlines()[1:]:
            gene = line.split('\t')[0]
            expression = line.split('\t')[2]

            if gene not in geneset:
                newgenes += 1
                genes.append(gene)
                geneset.add(gene)
                data[gene] = {}

            # TODO: Some files have duplicate genes; this logic considers
            # only the last occurrence of a gene in a file.
            data[gene][subpath_to_colname(subdir, filename)] = expression

        print '{} new genes'.format(newgenes)

count = 0
for gene in genes:
    count += 1
    if count % 100 == 0:
        print 'Adding gene {}'.format(count)
    cols = data[gene].keys()
    vals = [data[gene][key] for key in cols]
    add_gene_query = '''INSERT INTO rpkm(gene, {}) VALUES ('{}', '{}')'''.format(
        ', '.join(cols),    
        gene,
        '\', \''.join(vals),
    )
    c.execute(add_gene_query)

# Test the resulting database by printing the first few columns and rows
c.execute('''SELECT embryonic_deng_early2cell_GSM1112609, embryonic_deng_earlyblast_GSM1112627  FROM rpkm''')
print c.fetchmany(5)

conn.commit()
conn.close()

## Slower, less memory-intensive approach:
#
## Next, loop over raw data files to obtain gene names, which we do first
## to avoid needing to store the whole dataset in RAM
#genes = []
#for subdir in subdirs:
#    print 'Adding gene names from dataset {}...'.format(subdir)
#    for filename in filenames[subdir]:
#        print filename
#        geneset = set(genes)
#        newgenes = 0
#
#        f = open('{}/{}/{}'.format(pathbase, subdir, filename))
#        for line in f.readlines()[1:]:
#            gene = line.split('\t')[0]
#
#            if gene not in geneset:
#                newgenes += 1
#                genes.append(gene)
#                # TODO: Some files have duplicate genes; this logic considers
#                # only the first occurrence of a gene in a file.
#                geneset.add(gene)
#
#        print '{} new genes'.format(newgenes)
#
#for gene in genes:
#    add_gene_query = '''INSERT INTO rpkm(gene) VALUES ('{}')'''.format(gene)
#    c.execute(add_gene_query)
#
#print 'Row initialization complete.'
#
## Finally, loop over the data files a third time to add the relevant gene
## expression values
#for subdir in subdirs:
#    print 'Processing dataset {}...'.format(subdir)
#    count = 0
#    for filename in filenames[subdir]:
#        linecount = 0
#        print filename
#
#        f = open('{}/{}/{}'.format(pathbase, subdir, filename))
#        for line in f.readlines()[1:]:
#            gene = line.split('\t')[0]
#            expression = line.split('\t')[2]
#
#            update_query = '''UPDATE rpkm
#                SET {} = {}
#                WHERE gene == '{}'
#            '''.format(
#                subpath_to_colname(subdir, filename),
#                expression,
#                gene,
#            )
#
#            c.execute(update_query)
#            linecount += 1
#            if linecount % 100 == 0:
#                print 'Processing line {}'.format(linecount)
#        count += 1
#        if count > 5:
#            break
#
## Test the resulting database by printing the first few rows
#c.execute('''SELECT * FROM rpkm''')
#print c.fetchmany(5)
#
#conn.commit()
#conn.close()
