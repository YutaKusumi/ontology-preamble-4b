# -*- coding: utf-8 -*-
"""gate_null_sim.py —— B-lens 草案1 §4 の門（64 行・自由な並べ替え・Spearman 片側・Holm m=2）を、
合成の帰無と対立で走らせ、行の従属（同じ方向・同じ土台を分け合う）が偽の通過率をどれだけ上げるかの目安を出す。
設計の検分（第一巡・claude.ai の Claude Opus 5.5 の票）の根拠の置き場。

- 実データは一つも読まない。語彙の行列も方向も使わない（射影は計算しない）。
- 行の構造は転記行 D の内訳（Nk 8・loaded 1・rand 39・static 8・td 8）から推定して組んだ:
  場面ごとに static（O-Ncold−・Onull+）・td（同）・Nk（O-Ncold+・Onull+）・rand×3（O-Ncold−・Onull+・O-Ncold+）、
  S4 に loaded（Osec-Ncold+）と rand×3（同）。家族は N1＝nuclear・ほか survival。
- 帰無: 物差し M（方向 × 家族）と行動は独立。行動には方向ごとの効き b（符号で反転・家族間で相関）と、
  土台の揺れ（同じ土台の行で共有）と、行ごとの揺れ（件数 200 と 67 で幅を変える）がある。
- 比べる二つの並べ替え: 自由（64 行を混ぜる・草案の門）／方向を単位（7 方向の M を入れ替える・5040 通り）。
- 通過＝二つの物差しの小さい方の p が 0.025 以下（Holm m=2・水準 0.05）。
- 手元で得た目安（各 200 回・種 12345）:
    帰無 tau=0.0 自由 0.015／方向 0.045 ・ tau=0.3 自由 0.325／方向 0.040
         tau=0.5 自由 0.395／方向 0.060 ・ tau=0.8 自由 0.450／方向 0.035
    対立（M_L 役が方向の効きの幅 0.5 のうち 0.25／0.5／1.0 を担う）: 方向を単位の通過率 0.175／0.560／0.910
  行の構造と効きの大きさは仮定であり、値は目安にとどまる。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import numpy as np, itertools, time
from scipy.stats import rankdata
rng=np.random.default_rng(12345)
scenes=['N1','S1','SK','S4']; fam=lambda s: 0 if s=='N1' else 1
rows=[]
for s in scenes:
    rows+= [('static',-1,(s,'ONc')),('static',+1,(s,'On')),('td',-1,(s,'ONc')),('td',+1,(s,'On')),('Nk',+1,(s,'ONc')),('Nk',+1,(s,'On'))]
    for r in ('r0','r1','r2'): rows+= [(r,-1,(s,'ONc')),(r,+1,(s,'On')),(r,+1,(s,'ONc'))]
rows.append(('loaded',+1,('S4','OsNc')))
for r in ('r0','r1','r2'): rows.append((r,+1,('S4','OsNc')))
assert len(rows)==64
D=['static','loaded','Nk','td','r0','r1','r2']
bases=sorted(set(c for _,_,c in rows))
sign=np.array([s for _,s,_ in rows]); di=np.array([D.index(d) for d,_,_ in rows])
fi=np.array([fam(c[0]) for _,_,c in rows]); bi=np.array([bases.index(c) for _,_,c in rows])
nrow=np.array([200 if d in('static','loaded','Nk','td') else 67 for d,_,_ in rows])
P=np.array(list(itertools.permutations(range(7))))  # 5040
def corr_rows(X,y):  # X: (k,64) → Spearman with y
    RX=rankdata(X,axis=1); RX=RX-RX.mean(1,keepdims=True)
    ry=rankdata(y); ry=ry-ry.mean()
    return (RX@ry)/np.sqrt((RX*RX).sum(1)*(ry@ry))
def sim(tau,sig,bsd,nperm=999):
    b=rng.normal(0,tau,(7,2)); b[:,0]=0.7*b[:,1]+rng.normal(0,0.7*tau,7)
    base=rng.normal(0,bsd,len(bases))
    y=sign*b[di,fi]+base[bi]+rng.normal(0,sig,64)*np.sqrt(200/nrow)
    pf=[];pd=[]
    for k in range(2):
        M=rng.normal(0,1,(7,2)); M[:,0]=0.8*M[:,1]+rng.normal(0,0.6,7)
        x=sign*M[di,fi]; obs=corr_rows(x[None],y)[0]
        idx=np.argsort(rng.random((nperm,64)),axis=1)
        nf=corr_rows(x[idx],y); pf.append((1+(nf>=obs-1e-12).sum())/(1+nperm))
        Xd=sign[None]*M[P][:,di,fi]; nd=corr_rows(Xd,y); pd.append((nd>=obs-1e-12).mean())
    h=lambda ps: min(ps)<=0.025
    return h(pf),h(pd)
t=time.time()
for tau in (0.0,0.3,0.5,0.8):
    r=np.array([sim(tau,0.2,0.15) for _ in range(200)])
    print('方向の効きの幅 tau=%.1f（対数オッズ）: 偽の通過率 自由な並べ替え %.3f／方向を単位 %.3f'%(tau,r[:,0].mean(),r[:,1].mean()),flush=True)
print('sec',round(time.time()-t))

def sim_alt(lam,tau,sig,bsd,nperm=999):
    # 対立: 一つ目の物差し（M_L 役）が方向の効きに lam の重さで効く
    M1=rng.normal(0,1,(7,2)); M1[:,0]=0.8*M1[:,1]+rng.normal(0,0.6,7)
    M2=rng.normal(0,1,(7,2)); M2[:,0]=0.8*M2[:,1]+rng.normal(0,0.6,7)
    e=rng.normal(0,tau,(7,2))
    b=lam*M1*0.5+e
    base=rng.normal(0,bsd,len(bases))
    y=sign*b[di,fi]+base[bi]+rng.normal(0,sig,64)*np.sqrt(200/nrow)
    pf=[];pd=[]
    for M in (M1,M2):
        x=sign*M[di,fi]; obs=corr_rows(x[None],y)[0]
        idx=np.argsort(rng.random((nperm,64)),axis=1)
        nf=corr_rows(x[idx],y); pf.append((1+(nf>=obs-1e-12).sum())/(1+nperm))
        Xd=sign[None]*M[P][:,di,fi]; nd=corr_rows(Xd,y); pd.append((nd>=obs-1e-12).mean())
    return min(pf)<=0.025, min(pd)<=0.025
for lam in (0.5,1.0,2.0):
    r=np.array([sim_alt(lam,0.5,0.2,0.15) for _ in range(200)])
    print('対立 lam=%.1f（方向の効きの幅 0.5 のうち物差しが担う分 %.2f）: 通過率 自由 %.3f／方向を単位 %.3f'%(lam,0.5*lam,r[:,0].mean(),r[:,1].mean()),flush=True)
