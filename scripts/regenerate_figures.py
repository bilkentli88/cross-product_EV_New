"""Regenerate the two manuscript figures from the saved verified product means."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parents[1]
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir', type=Path, default=root/'generated_figures')
args=parser.parse_args()
dest=args.output_dir.resolve()
dest.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':14,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42})
colors=['#243c61','#158677']
agg=pd.read_csv(root/'results/principal/e10/e10_aggregate.csv').set_index('condition')
variants=['Static','GlobalOnly','GlobalStatus','GlobalStructure','Full']
fig,ax=plt.subplots(figsize=(7.0,3.8),layout='constrained')
y=np.arange(len(variants))
for j,l in enumerate(['MLP','XGB']):
    vals=np.array([100*agg.loc[v+l,'hits1'] for v in variants])
    offset=(j-.5)*.34
    ax.scatter(vals,y+offset,s=48,color=colors[j],label=l,zorder=3)
    for val,pos in zip(vals,y+offset): ax.annotate(f'{val:.2f}',(val,pos),xytext=(6,0),textcoords='offset points',va='center',fontsize=12)
ax.set(yticks=y,yticklabels=variants,xlim=(34.5,45),xlabel='Mean product Hits@1 (%)')
ax.invert_yaxis();ax.grid(axis='x',alpha=.18);ax.legend(loc='upper left',bbox_to_anchor=(.0,1.2),ncol=2,frameon=False,fontsize=12)
fig.savefig(dest/'e10_feature_families.pdf');fig.savefig(dest/'e10_feature_families.png',dpi=220);plt.close(fig)

prod=pd.read_csv(root/'results/principal/e11/e11_fold_mean.csv').pivot(index=['battery_id','battery'],columns='family',values='hits1').sort_index()
fig,axs=plt.subplots(1,2,figsize=(7.7,5.8),sharey=True,layout='constrained')
for j,(control,ax) in enumerate(zip(['ActiveShuffle','NoEdge'],axs)):
    vals=100*(prod.Real-prod[control]).values
    ax.axvline(0,color='#505b68',linewidth=.8)
    ax.hlines(np.arange(10),0,vals,color=colors[j],alpha=.45,linewidth=2)
    ax.scatter(vals,np.arange(10),s=36,color=colors[j],zorder=3)
    ax.axvline(vals.mean(),color=colors[j],linestyle='--',linewidth=1,label=f'Mean: {vals.mean():.2f} pp')
    ax.set(title='Real minus\n'+control,xlim=(-.75,17.5),xticks=[0,5,10,15],ylim=(10.2,-.5))
    for val,pos in zip(vals,np.arange(10)): ax.annotate(f'{val:+.2f}',(val,pos),xytext=(5,0),textcoords='offset points',va='center',fontsize=12,bbox={'facecolor':'white','edgecolor':'none','pad':0.1})
    ax.grid(axis='x',alpha=.16);ax.legend(loc='lower right',fontsize=11,frameon=False)
axs[0].set(yticks=np.arange(10),yticklabels=prod.index.get_level_values('battery').tolist())
fig.supxlabel('Hits@1 difference (percentage points)',fontsize=14)
fig.savefig(dest/'e11_product_differences.pdf');fig.savefig(dest/'e11_product_differences.png',dpi=220);plt.close(fig)

print('Figures written to', dest)
