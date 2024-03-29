import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import seaborn as sns

import matplotlib.patheffects as PathEffects
sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5,
                rc={"lines.linewidth": 2.5})
RS = 123

def fashion_scatter(x, colors):
    # choose a color palette with seaborn.
    num_classes = len(np.unique(colors))
    palette = np.array(sns.color_palette("hls", num_classes))

    # create a scatter plot.
    f = plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    sc = ax.scatter(x[:,0], x[:,1], lw=0, s=40, c=palette[colors.astype(np.int)])
    plt.xlim(-25, 25)
    plt.ylim(-25, 25)
    ax.axis('off')
    ax.axis('tight')

    # add the labels for each digit corresponding to the label
    txts = []

    for i in range(num_classes):

        # Position of each label at median of data points.

        xtext, ytext = np.median(x[colors == i, :], axis=0)
        txt = ax.text(xtext, ytext, str(i), fontsize=24)
        txt.set_path_effects([
            PathEffects.Stroke(linewidth=5, foreground="w"),
            PathEffects.Normal()])
        txts.append(txt)

    return f, ax, sc, txts

from sklearn.cluster import KMeans
def _clustering(data,cn):
    kmeans=KMeans(n_clusters=cn)
    results=kmeans.fit(data[:,1:])
    labels = kmeans.labels_


    return results, labels

def pca_f(data, plot = False, transform = True, dims):
    '''
    PCA
    '''
    if plot:
        explained_variance_variation = []
        for i in range(1, data.shape[1]):
            pca = PCA(n_components = i)
            test=pca.fit(data[:,1:])  
            #print 'cur importance',pca.explained_variance_ratio_

            explained_variance_variation.append(sum(pca.explained_variance_ratio_))

            #print 'accumutaed',explained_variance_variation     
        '''
        This plot visualizes the total explained variance with the number of reduced dimensions
        ''' 
        plt.scatter([i for i in range(1,data.shape[1] )], explained_variance_variation, alpha = 0.3, color = 'red')
        plt.xlabel("Number of components")
        plt.ylabel("Total explained variance")
        plt.title("Total explained variance vs number of components")
        return np.where(np.array(explained_variance_variation)>0.9)[-1]

    if transform: 

        column_header=[]
        for i in range(dims):
            a='pca'+str(i)
            column_header.append(a)

        pca_df = pd.DataFrame(columns = column_header)
        pca = PCA(n_components = dims)
        embeddings_pca = pca.fit_transform(data[:,1:])

        return embeddings_pca


#         embeddings_pca_flattened = embeddings_pca.flatten('F')
#         plt.scatter(embeddings_pca_flattened[:1234], embeddings_pca_flattened[1234:], alpha = 0.3, color = 'purple')

def tsne_f(embeddings,y):
    '''
    Visualize t-SNE embeddings of the embeddings
    '''
    plt.clf()

    X_embedded = TSNE(n_components=2, perplexity = 20, metric = 'cityblock').fit_transform(embeddings)
    X_embedded_flattened = X_embedded.flatten('F')   
    fashion_scatter(np.array(X_embedded), y)
    return X_embedded,X_embedded_flattened
if __name__ == "__main__":
data=np.load(r'transition_probability.npy')
dims=pca_f(data, plot = True, transform = False,0)
results=pca_f(data, plot = False, transform = True, dims)#the first two components explained 0.6616 and 0.198=0.785
#----Visulazation high-demension groups results and decide K
 #------------using projected new feature demionsion to kmeans#using unprojected raw data to show the group results
 for i in range(2,5):
    cluster_results=_clustering(results,i)
    tsne_f(data[:,1:],cluster_results[1])
