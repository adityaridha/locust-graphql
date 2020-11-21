from locust import HttpUser, TaskSet, task, between


class UserTask(TaskSet):

    def graphql_request(self, query, variable, name):
        with self.client.post(url="", json={'query': query, 'variables': variable}, catch_response=True,
                              name=name) as response:
            print(response.text)
            if response.status_code != 200:
                response.failure("Something when wrong")

    @task(1)
    def claim_query(self):
        query = """
        {
            claims{
               count,
                result{
                  id,
                  assetNumber,
                  dateOfLoss,
                  dateOfNotification,
                  sheproReference,
                  status,
                  statusCode,
                  createdOn,
                  claimNumber
                }
            }
         }
         """

        self.graphql_request(query=query, variable={}, name="claim query")

    @task(1)
    def claim_submit(self):
        query = """
            mutation($claimInput: ClaimInput!) {
              submitClaim(claimInput: $claimInput) {
                claimNumber
              }
            }
         """

        variable =  {
              "claimInput" : {
                  "causeOfLoss": "teuing 2",
                  "chronology": "blablbalablabla",
                  "claimDescription": "claim description",
                  "dateOfLoss": "2020-11-11T00:00:00",
                  "dateOfNotification": "2020-11-11T00:00:00",
                  "division": "division",
                  "divisionId": 1,
                  "divisionManager": "Marlina",
                  "divisionManagerId": "61988bdc-5a1e-4c37-8cf0-66a64311deb9",
                  "location": "ga tau juga yah",
                  "project": "apa ini",
                  "id": "893e2c14-7b9b-4ce3-97ee-bf753ba62973",
                  "requestorId": "61988bdc-5a1e-4c37-8cf0-66a64311deb9",
                  "requestorName": "Marlina",
                  "sheproRef": "sheproRef",
                  "status": "Drafted",
                  "statusCode": "RequestorDraft",
                  "type": "Shipment Insurance",
                  "supportingDocuments": [],
                  "pictureOfDamages": [],
                  "claimDetails": [
                    {
                      "accumulatedAdjustedClaim": "safas0d",
                      "adjustedClaim": "adsad",
                      "approvedClaim": "asfasdas",
                      "assetNumber": "12124342",
                      "costCode": "babababa",
                      "deductible": 100,
                      "estLoss": "jsadas",
                      "id": "40e599ac-e6fc-42bb-b3c0-fd3a00df1566",
                      "insuranceSubType": "Marine Cargo",
                      "lossOfConsequence": "teuing",
                      "policyNumber": "zzzzzzzz",
                      "workOrderNumber": None
                    }
                  ]
              }
            }

        self.graphql_request(query=query, variable=variable, name="claim submit")

class UserDemo(HttpUser):
    host = 'http://128.199.80.153:31120/graphql'
    tasks = [UserTask]
    wait_time = between(1, 2)