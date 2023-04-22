                        maind = StrawBerry(have_data=False,fp=f".\\{dbname}.BerryBase\\{name}.berrybase")
                        
                        maind = maind.update((maind.punnet[maind.PRIMARY_KEY].vals).index(d[maind.PRIMARY_KEY]),d)
                        p= maind['hull']['primary_key']
                        maind['mainfruit'].update({d[p]:d})