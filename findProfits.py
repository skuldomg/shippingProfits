import json, csv, operator, math, platform

debug = False

# Use correct filepath separators for different OSes
if "Windows" in platform.system():
    sep = "\\"
else:
    sep = "/"

with open('profits.csv', mode='w', newline='') as ag:
    agWriter = csv.writer(ag, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)    
    agWriter.writerow(['Product', 'Volume || weight', 'Units/ship', 'Ask Katoa', 'Bid Katoa', 'Ask Prom', 'Bid Prom', 'Ask Montem', 'Bid Montem', '', 'Kat -> Prom', 'Kat -> Montem', 'Prom -> Kat', 'Prom -> Montem', 'Montem -> Kat', 'Montem -> Prom', '', 'Best route', 'Max sales/ship', 'Investment'])
    
    def empty_if_negative(val):
        if(val <= 0):
            val = ""
            
        return val
    
    def get_row(product):        
        # Get weight/volume
        weight = float(data["comex"]["broker"]["brokers"][product+".CI1"]["data"]["material"]["weight"])
        volume = float(data["comex"]["broker"]["brokers"][product+".CI1"]["data"]["material"]["volume"])
        weightOrVol = -1.0
        if(weight > volume):
            weightOrVol = weight
        else:
            weightOrVol = volume
        
        # Check if asks/bids exist
        if data["comex"]["broker"]["brokers"][product+".CI1"]["data"]["ask"]:
            katAsk = int(data["comex"]["broker"]["brokers"][product+".CI1"]["data"]["ask"]["price"]["amount"])
        else:
            katAsk = -1
            
        if data["comex"]["broker"]["brokers"][product+".CI1"]["data"]["bid"]:
            katBid = int(data["comex"]["broker"]["brokers"][product+".CI1"]["data"]["bid"]["price"]["amount"])
        else:
            katBid = -1
            
        if data["comex"]["broker"]["brokers"][product+".IC1"]["data"]["ask"]:
            promAsk = int(data["comex"]["broker"]["brokers"][product+".IC1"]["data"]["ask"]["price"]["amount"])
        else:
            promAsk = -1
            
        if data["comex"]["broker"]["brokers"][product+".IC1"]["data"]["bid"]:
            promBid = int(data["comex"]["broker"]["brokers"][product+".IC1"]["data"]["bid"]["price"]["amount"])
        else:
            promBid = -1
            
        if data["comex"]["broker"]["brokers"][product+".NC1"]["data"]["ask"]:
            montAsk = int(data["comex"]["broker"]["brokers"][product+".NC1"]["data"]["ask"]["price"]["amount"])
        else:
            montAsk = -1
            
        if data["comex"]["broker"]["brokers"][product+".NC1"]["data"]["bid"]:
            montBid = int(data["comex"]["broker"]["brokers"][product+".NC1"]["data"]["bid"]["price"]["amount"])
        else:
            montBid = -1
            
        # bidDest - askSource = sales
        # Determine sales
        # Kat -> Prom
        if(promBid > 0 and katAsk > 0):
            katProm = promBid - katAsk
        else:
            katProm = -1
            
        # Kat -> Mont
        if(montBid > 0 and katAsk > 0):
            katMont = montBid - katAsk
        else:
            katMont = -1
            
        # Prom -> Kat
        if(katBid > 0 and promAsk > 0):
            promKat = katBid - promAsk
        else:
            promKat = -1
            
        # Prom -> Mont
        if(montBid > 0 and promAsk > 0):
            promMont = montBid - promAsk
        else:
            promMont = -1
            
        # Mont -> Kat
        if(katBid > 0 and montAsk > 0):
            montKat = katBid - montAsk
        else:
            montKat = -1
            
        # Mont -> Prom
        if(promBid > 0 and montAsk > 0):
            montProm = promBid - montAsk
        else:
            montProm = -1
            
        # Find max profit
        #profitList = [katProm, katMont, promKat, promMont, montKat, montProm]
        profitDict = {
            "Kat -> Prom": katProm,
            "Kat -> Mont": katMont,
            "Prom -> Kat": promKat,
            "Prom -> Mont": promMont,
            "Mont -> Kat": montKat,
            "Mont -> Prom": montProm
        }
        
        # Find best route and corresponding profit per unit
        bestRoute = max(profitDict.items(), key=operator.itemgetter(1))[0]
        maxPPU = profitDict.get(bestRoute)
        
        if debug:
            print("Best route: "+bestRoute+" with ppu: "+str(maxPPU))
            
        # Figure out where the best buy was
        if(bestRoute.startswith("Kat")):
            bestBuy = katAsk
        elif(bestRoute.startswith("Prom")):
            bestBuy = promAsk
        elif(bestRoute.startswith("Mont")):
            bestBuy = montAsk
            
        if(maxPPU <= 0):
            bestRoute = ""
        
        maxPerShip = math.floor(400/weightOrVol)
        maxSales = round(maxPPU*maxPerShip, 2)
        
        if("->" in bestRoute):
            investment = round(bestBuy*maxPerShip, 2)
        else:
            investment = -1
        
        # Don't print negative numbers so that the table isn't cluttered as much
        katAsk = empty_if_negative(katAsk)
        katBid = empty_if_negative(katBid)
        promAsk = empty_if_negative(promAsk)
        promBid = empty_if_negative(promBid)
        montAsk = empty_if_negative(montAsk)
        montBid = empty_if_negative(montBid)
        katProm = empty_if_negative(katProm)
        katMont = empty_if_negative(katMont)
        promKat = empty_if_negative(promKat)
        promMont = empty_if_negative(promMont)
        montKat = empty_if_negative(montKat)
        montProm = empty_if_negative(montProm)
        maxSales = empty_if_negative(maxSales)
        investment = empty_if_negative(investment)
        
        # Write line
        agWriter.writerow([product, weightOrVol, maxPerShip, katAsk, katBid, promAsk, promBid, montAsk, montBid,"",
            katProm, katMont, promKat, promMont, montKat, montProm,"",bestRoute,maxSales,investment])
    
    try:
        with open('brokerdata'+sep+'brokerdataAgriculture.json', encoding='utf8') as f:            
            try:
                data = json.load(f)
                agWriter.writerow(["Agricultural Products"])
                get_row("HOP")
                get_row("CAF")
                get_row("GRN")
                get_row("MAI")
                get_row("RCO")
                get_row("NUT")
                get_row("VEG")
                get_row("GRA")
                get_row("HER")
                get_row("HCP")
                get_row("MTP")
                get_row("ALG")
                get_row("BEA")
                get_row("PPA")
                get_row("RSI")
                agWriter.writerow([""])

            except:
                if(debug):
                    print("Empty JSON. Skipping...")
            
            f.close()

    except EnvironmentError:
        if debug:
            print("No data, skipping...")

    try:
        with open('brokerdata'+sep+'brokerdataAlloys.json', encoding='utf8') as f:
            try:
                data = json.load(f)
                agWriter.writerow(["Alloys"])
                get_row("BTI")
                get_row("AST")
                get_row("BRO")
                get_row("RGO")
                get_row("BGO")
                get_row("FET")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")
            
            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataConsumables.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Basic Consumables"])
                get_row("DW")
                get_row("HSS")
                get_row("FIM")
                get_row("PDA")
                get_row("OVE")
                get_row("RAT")
                get_row("LC")
                get_row("MEA")
                get_row("WS")
                get_row("EXO")
                get_row("PT")
                get_row("HMS")
                get_row("MED")
                get_row("SCN")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")
                    
            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")

    try:
        with open('brokerdata'+sep+'brokerdataChemicals.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Chemicals"])
                
                get_row("BAC")
                get_row("BLE")
                get_row("BL")
                get_row("CST")
                get_row("FLX")
                get_row("IND")
                get_row("LCR")
                get_row("NR")
                get_row("NS")
                get_row("DDT")
                get_row("TCL")
                get_row("THF")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")
                    
            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")        
            
    try:
        with open('brokerdata'+sep+'brokerdataConstructionMaterials.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Construction Materials"])
                
                get_row("EPO")
                get_row("INF")
                get_row("MTC")
                get_row("MCG")
                get_row("NCS")
                get_row("NFI")
                get_row("NG")
                get_row("RG")
                get_row("SEA")
                get_row("GL")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")
            
            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataConstructionParts.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Construction Parts"])
                
                get_row("AEF")
                get_row("AIR")
                get_row("FC")
                get_row("FLP")
                get_row("GC")
                get_row("GV")
                get_row("MGC")
                get_row("MHL")
                get_row("PSH")
                get_row("RSH")
                get_row("TCS")
                get_row("TSH")
                get_row("TRU")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")
                    
            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataConstructionPrefabs.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Construction Prefabs"])
                
                get_row("ABH")
                get_row("ADE")
                get_row("ASE")
                get_row("ATA")
                get_row("BBH")
                get_row("BDE")
                get_row("BSE")
                get_row("BTA")
                get_row("HSE")
                get_row("LBH")
                get_row("LDE")
                get_row("LSE")
                get_row("LTA")
                get_row("RBH")
                get_row("RDE")
                get_row("RSE")
                get_row("RTA")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")
                    
            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataElectronicDevices.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Electronic Devices"])
                
                get_row("HD")
                get_row("BMF")
                get_row("PA")
                get_row("SAR")
                get_row("HPC")
                get_row("DIS")
                get_row("AWF")
                get_row("BWS")     
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")
                    
            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataElectronicParts.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Electronic Parts"])
                
                get_row("FAN")
                get_row("EBS")
                get_row("RAM")
                get_row("MPC")
                get_row("MB")
                get_row("ROM")
                get_row("PCB")
                get_row("SEN")
                get_row("SP")
                get_row("SOC")
                get_row("TPU")
                get_row("CD")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")

            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataElectronicPieces.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Electronic Pieces"])
                
                get_row("BGC")
                get_row("CAP")
                get_row("BCO")
                get_row("MFK")
                get_row("SFK")
                get_row("LDI")
                get_row("HCC")
                get_row("TRN")
                get_row("MWF")
                get_row("SWF")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")

            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")            
        
    try:
        with open('brokerdata'+sep+'brokerdataElectronicSystems.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Electronic Systems"])
                
                get_row("CC")
                get_row("CRU")
                get_row("FFC")
                get_row("LIS")
                get_row("TAC")
                get_row("WR")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")

            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataElements.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Elements"])
                
                get_row("BE")
                get_row("CA")
                get_row("C")
                get_row("CL")
                get_row("ES")
                get_row("I")
                get_row("NA")
                get_row("TA")
                get_row("TC")
                get_row("W")
                get_row("ZR")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")

            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataFuel.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Fuel"])
                
                get_row("FF")
                get_row("SF")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")

            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataGases.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Gases"])
                
                get_row("AMM")
                get_row("AR")
                get_row("F")
                get_row("HE")
                get_row("HE3")
                get_row("H")
                get_row("NE")
                get_row("N")
                get_row("O")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")

            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataLiquids.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Liquids"])
                
                get_row("LES")
                get_row("BTS")
                get_row("H2O")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")

            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataLuxuryConsumables.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Luxury Consumables"])
                
                get_row("GIN")
                get_row("VG")
                get_row("PWO")
                get_row("COF")
                get_row("WIN")
                get_row("NST")
                get_row("KOM")
                get_row("REP")
                get_row("ALE")
                get_row("SC")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")

            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataMetals.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Metals"])
                
                get_row("AL")
                get_row("CU")
                get_row("AU")
                get_row("FE")
                get_row("SI")
                get_row("STL")
                get_row("TI")
                agWriter.writerow([""])

            except:
                if(debug):
                    print("Empty JSON. Skipping...")

            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataMinerals.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Minerals"])
                
                get_row("BER")
                get_row("CLI")
                get_row("GAL")
                get_row("HAL")
                get_row("LST")
                get_row("MG")
                get_row("MAG")
                get_row("S")
                get_row("TAI")
                get_row("TCO")
                get_row("TS")
                get_row("ZIR")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")

            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataOres.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Ores"])
                
                get_row("ALO")
                get_row("CUO")
                get_row("AUO")
                get_row("FEO")
                get_row("SIO")
                get_row("TIO")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")

            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataPlastics.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Plastics"])
                
                get_row("DCL")
                get_row("PSL")
                get_row("DCM")
                get_row("PSM")
                get_row("PE")
                get_row("PG")
                get_row("DCS")
                get_row("PSS")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")

            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataShipParts.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Ship Parts"])
                
                get_row("NV1")
                get_row("NV2")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")

            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataSoftware.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Software"])
                
                get_row("CNN")
                get_row("DA")
                get_row("DV")
                get_row("DD")
                get_row("FNN")
                get_row("LD")
                get_row("NF")
                get_row("OS")
                get_row("RA")
                get_row("RNN")
                get_row("SA")
                get_row("SAL")
                get_row("SNM")
                get_row("WAI")
                get_row("WM")
                agWriter.writerow([""])
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")

            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")
        
    try:
        with open('brokerdata'+sep+'brokerdataTextiles.json', encoding='utf8') as f:
            try:
                data = json.load(f)            
                agWriter.writerow(["Textiles"])
                
                get_row("COT")
                get_row("KV")
                get_row("NL")
                get_row("SIL")
                get_row("TK")
            
            except:
                if(debug):
                    print("Empty JSON. Skipping...")

            f.close()
    except EnvironmentError:
        if debug:
            print("No data, skipping...")