import weclapp as wc

def cache_all_wc_data():
    """Cache all data from WeClapp to local database"""
    with wc.WcCacheWrapper() as wrapper:
        wrapper.cache_all()

if __name__ == "__main__":
    cache_all_wc_data()