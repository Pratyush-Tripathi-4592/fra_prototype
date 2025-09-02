def recommend(record, water_index=0.1):
    recs = []
    if water_index < 0.2 and record.get('land_size',0) > 0.2:
        recs.append({'scheme':'Jal Shakti (borewell)','reason':'Low water index & farmland'})
    if record.get('landholding_type')=='smallholder' and record.get('is_farmer'):
        recs.append({'scheme':'PM-KISAN','reason':'Farmer with small landholding'})
    return recs

if __name__ == "__main__":
    # demo
    recs = recommend({'land_size':0.5,'landholding_type':'smallholder','is_farmer':True}, water_index=0.1)
    print(recs)
