from pathlib import Path
import data.aDataLoadAndCleaningHistorical as DataLoad
import data.bDataEnrichment as DataEnrichment
import features.RidingPatternsPlots as Plots
import visualization.NetArivalsDepartures


def main(dir, year):
    DataLoad.main(dir, year)
    DataEnrichment.main(dir, year)
    Plots.plots(dir)

if __name__ == "__main__":
    dataYear = input("Please chose year fo analysis (2015 or 2016) \n")
    project_dir = str(Path(__file__).resolve().parents[1])
    main(project_dir, dataYear)