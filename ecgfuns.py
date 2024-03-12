from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
from scipy.signal import resample

'''
addFilteredData takes a column in a DataFrame, and returns the same DataFrame
adding a column <columnName>_dns with PCA-filtered data.
'''
def addFilteredData(a: pd.DataFrame, field: str, comps = 3):
    rpeaks = a.query('ECG_peaks == 1').index.tolist()
    signal = a[field].to_numpy()
    
    r2r = [(i,j) for i,j in zip(rpeaks[:-1], rpeaks[1:])]
    r2r_dist = [j-i for i,j in r2r]
    avg_dist = int(np.mean(r2r_dist) + 0.5)
    ori_signals = [signal[i:j] for i,j in r2r]
    resampled_templates = [resample(signal[i:j],avg_dist) for i,j in r2r]
    print('Mean len of RR interval: ', avg_dist)
    
    ## Apply PCA and transform
    pca_ = PCA(n_components=comps)
    transformed_resampled_templates = pca_.fit_transform(resampled_templates)
    ## Retransform the templates and restitch
    retransformed_templates = [resample(i,j) for i,j in 
            zip(pca_.inverse_transform(transformed_resampled_templates),r2r_dist)]
    restitched_signal = np.concatenate(retransformed_templates)
    
    _a = a.copy()
    # add new column to the source DF
    _a[field + "_dns"] = 0.0
    _a.loc[rpeaks[0]:rpeaks[-1]-1, field + "_dns"] = restitched_signal
    return _a

'''
addFilteredDataE adds filtered column, doing PCA independently for paced and controlled part. 
It is required if the average width of R-R interval differs significantly, because
the position of P-peak is not relative. It is absolute to the next R-peak. But PCA-filtering
works in that way that it remove noise considering relative position of feeatures preserve themself.
'''
def addFilteredDataE(a: pd.DataFrame, field: str, comps = 3):
    rpeaks = a.query('ECG_peaks == 1').index.tolist()
    lpeaks = a.query('Las_peaks == 1').index.tolist()
    signal = a[field].to_numpy()
    
    r2r = [(i,j) for i,j in zip(rpeaks[:-1], rpeaks[1:])]
    
    r2r_p = []
    r2r_c = []
    for i,j in r2r:
        if (j > lpeaks[5]) and (i < lpeaks[-5]):
            r2r_p.append( (i,j) )
        else:
            r2r_c.append( (i,j) )
            
    sigpatches = []        
    for r2r in [r2r_p, r2r_c]:
        r2r_dist = [j-i for i,j in r2r]
        avg_dist = int(np.mean(r2r_dist) + 0.5)
        ori_signals = [signal[i:j] for i,j in r2r]
        resampled_templates = [resample(signal[i:j],avg_dist) for i,j in r2r]
        print('Mean len of RR interval: ', avg_dist)

        ## Apply PCA and transform
        pca_ = PCA(n_components=comps)
        transformed_resampled_templates = pca_.fit_transform(resampled_templates)
        ## Retransform the templates and restitch
        retransformed_templates = [resample(i,j) for i,j in 
                zip(pca_.inverse_transform(transformed_resampled_templates),r2r_dist)]
        sigpatches += zip([i for i,j in r2r], retransformed_templates)
    
    restitched_signal = np.concatenate([j for i,j in sorted(sigpatches)])
    
    _a = a.copy()
    # add new column to the source DF
    _a[field + "_dns"] = 0.0
    _a.loc[rpeaks[0]:rpeaks[-1]-1, field + "_dns"] = restitched_signal
    return _a

'''
Generate phasic informations for events in ECG. See the commented sample for the explanations.
'''
def genPhaseData(b, rpks):
    dats = []
    c = 0
    for i,j in list(zip(rpks[:-1], rpks[1:])):
        c += 1
        ppk = b.loc[i:j,:].query('P_peaks == 1')
        pW = np.nan
        if (ppk.shape[0] == 1):
            pid = ppk.index[0]
            pW = ( (pid-i + int((j-i)/2) ) % (j-i) - int((j-i)/2) ) / (j-i) * 360.
            #print((j-pid)/(j-i)*360)
            dats.append( [c, 'p', pW, (j-i)/10] )
        lpk = b.loc[i:j,:].query('Las_peaks == 1')
        pL = np.nan
        if (lpk.shape[0] > 0):
            for l in lpk.index:
                pL = ( (l-i + int((j-i)/2) ) % (j-i) - int((j-i)/2) ) / (j-i) * 360. 
                dats.append( [c, 'laser', pL, (j-i)/10] )
                lpkE = b.loc[l:l+(j-i),:].query('Las_peaks == -1').index[0]
                pE = pL + (lpkE-l) / (j-i) * 360. 
                dats.append( [c, 'lasend', pE, (j-i)/10] )
        # print('%.1f' % (pW) )
        # print('%.1f' % (pL) )
    rads = pd.DataFrame(dats, columns=['i', 'type', 'phase', 'period'])
    return rads