import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from pyesgf.search import SearchConnection # import ESGF search tool from the ESGF Pyclient
    
conn = SearchConnection('https://esgf.ceda.ac.uk/esg-search',
                        distrib=True)

def search_pmip(variabl,experimen,modl=[]):
    if len(modl)==0:
        ctx = conn.new_context(project='PMIP3', experiment=experimen,variable=variabl,cmor_table='Oclim',facets='*') 
    else:
        with warnings.catch_warnings(record=True):
            ctx = conn.new_context(project='PMIP3', experiment=experimen,model=modl,variable=variabl,cmor_table='Oclim',facets='*') 

    return(ctx)



def get_pmip(variabl,experimen,modl):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ctx = search_pmip(modl=modl, experimen=experimen,variabl=variabl);
        result = ctx.search()[0];
    files = result.file_context().search();
    
    ifin_str = '/%s/' %variabl
    for file in files:
        if ifin_str in file.opendap_url:
            o_url = file.opendap_url
      
    return o_url

import xarray as xr

def area_weighted_average(df,dim, weights):
    '''function is modified after the extremely useful tutorial found at https://nordicesmhub.github.io/NEGI-Abisko-2019/training/Example_model_global_arctic_average.html'''
    df_copy = df.copy()
    _, weights_all_dims = xr.broadcast(df, weights)  # broadcast to all dims
    x_times_w = df_copy * weights_all_dims
    xw_sum = x_times_w.sum(dim)
    x_tot = weights_all_dims.where(df_copy.notnull()).sum(dim=dim)
    xa_weighted_average = xw_sum / x_tot
    return xa_weighted_average