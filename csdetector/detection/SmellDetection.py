import csv
import os
from joblib import load
import pandas as pd
from datetime import datetime
from pandas.core.dtypes.dtypes import pytz

from csdetector import Configuration

COMMUNITY_SMELLS = [
    {"acronym": "OSE", "name": "Organizational Silo Effect"},
    {"acronym": "BCE", "name": "Black-cloud Effect"},
    {"acronym": "PDE", "name": "Prima-donnas Effect"},
    {"acronym": "SV", "name": "Sharing Villainy"},
    {"acronym": "OS", "name": "Organizational Skirmish"},
    {"acronym": "SD", "name": "Solution Defiance "},
    {"acronym": "RS", "name": "Radio Silence"},
    {"acronym": "TF", "name": "Truck Factor Smell"},
    {"acronym": "UI", "name": "Unhealthy Interaction"},
    {"acronym": "TC", "name": "Toxic Communication"},
]

class SmellDetection:
    @classmethod
    def smellDetection(cls, config: Configuration, batchIdx: int):
        # prepare results holder for easy mapping
        results = {}

        # open finalized results for reading
        project_csv_path = os.path.join(config.resultsPath, f"results_{batchIdx}.csv")
        with open(project_csv_path, newline="") as csvfile:
            rows = csv.reader(csvfile, delimiter=",")

            # parse into a dictionary
            for row in rows:
                results[row[0]] = row[1]

        # map results to a list suitable for model classification
        metrics = cls.buildMetricsList(results)

        # load all models
        smells = ["OSE", "BCE", "PDE", "SV", "OS", "SD", "RS", "TF", "UI", "TC"]
        all_models = {}
        for smell in smells:
            modelPath = os.path.abspath("./models/{}.joblib".format(smell))
            all_models[smell] = load(modelPath)

        # detect smells
        rawSmells = {smell: all_models[smell].predict(metrics) for smell in all_models}
        detectedSmells = [smell for smell in smells if rawSmells[smell][0] == 1]

        # add last commit date as first output param
        #if config.endDate is not None:
        #    detectedSmells.insert(0, config.endDate)
        #else:    
        detectedSmells.insert(0, results["LastCommitDate"])

        # returning detected smells to devNetwork to handle output
        return detectedSmells

    @staticmethod
    def buildMetricsList(results: dict):
        # declare names to extract from the results file in the right order
        names = [
            "AuthorCount",
            "DaysActive",
            "CommitCount",
            "AuthorCommitCount_stdev",
            "commitCentrality_NumberHighCentralityAuthors",
            "commitCentrality_PercentageHighCentralityAuthors",
            "SponsoredAuthorCount",
            "PercentageSponsoredAuthors",
            "NumberPRs",
            "PRParticipantsCount_stdev",
            "PRParticipantsCount_mean",
            "NumberIssues",
            "IssueParticipantCount_stdev",
            "IssueCountPositiveComments_mean",
            "commitCentrality_Centrality_count",
            "commitCentrality_Centrality_stdev",
            "commitCentrality_Betweenness_count",
            "commitCentrality_Closeness_count",
            "commitCentrality_Density",
            "commitCentrality_CommunityAuthorCount_count",
            "commitCentrality_CommunityAuthorItemCount_mean",
            "commitCentrality_CommunityAuthorItemCount_stdev",
            "commitCentrality_CommunityAuthorCount_mean",
            "commitCentrality_CommunityAuthorCount_stdev",
            "TimezoneCount",
            "TimezoneCommitCount_mean",
            "TimezoneCommitCount_stdev",
            "TimezoneAuthorCount_mean",
            "TimezoneAuthorCount_stdev",
            "NumberReleases",
            "ReleaseCommitCount_mean",
            "ReleaseCommitCount_stdev",
            "FN",
            "PRDuration_mean",
            "IssueDuration_mean",
            "BusFactorNumber",
            "commitCentrality_TFN",
            "commitCentrality_TFC",
            "PRCommentsCount_mean",
            "PRCommitsCount_mean",
            "NumberIssueComments",
            "IssueCommentsCount_mean",
            "IssueCommentsCount_stdev",
            "PRCommentsToxicityPercentage",
            "IssueCommentsToxicityPercentage",
            "RPCPR",
            "RPCIssue",
            "IssueCountNegativeComments_mean",
            "PRCountNegativeComments_mean",
            "ACCL"
        ]

        # build key/value list
        metrics = []
        for name in names:

            # default value if key isn't present or the value is blank
            result = results.get(name, 0)
            if not result:

                print(f"No value for '{name}' during smell detection, defaulting to 0")
                result = 0

            metrics.append(result)

        # return as a 2D array
        return [metrics]


    # converting community smell acronym in full name
    @staticmethod
    def get_community_smell_name(smell):
        for sm in COMMUNITY_SMELLS:
            if sm["acronym"] == smell:
                return sm["name"]
        return smell

    # collecting execution data into a dataset
    @staticmethod
    def add_to_smells_dataset(config, starting_date, detected_smells):
        path_Smells = os.getcwd()
        
        with pd.ExcelWriter(path_Smells + '/out/Smells.xlsx', engine="openpyxl", mode='a', if_sheet_exists="overlay") as writer:
            
            series = { 
                      "Smells" : pd.Series([config.repositoryUrl, config.repositoryName, config.repositoryOwner, starting_date, str(detected_smells.count('OSE')),
                                            str(detected_smells.count('BCE')), str(detected_smells.count('PDE')), str(detected_smells.count('SV')),
                                            str(detected_smells.count('OS')), str(detected_smells.count('SD')), str(detected_smells.count('RS')),
                                            str(detected_smells.count('TF')), str(detected_smells.count('UI')), str(detected_smells.count('TC'))],
                                            index = ["RepositoryURL", "RepositoryName", "RepositoryOwner", "StartingDate", "OSE", "BCE", "PDE", "SV", "OS", "SD", "RS", "TF", "UI", "TC"])
                    }
            dataframe = pd.DataFrame(series)

            dataframe.to_excel(writer, sheet_name="dataset", header=False)