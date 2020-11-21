from locust import HttpUser, task, between, TaskSet


class UserTask1(TaskSet):

    def graphql_request(self, query, variable, name):

        with self.client.post(url="", json={'query': query, 'variables': variable}, catch_response=True,
                              name=name) as response:
            print(response.text)
            if response.status_code != 200:
                response.failure("Something when wrong")

    @task(0)
    def get_countries(self):
        query = """
            {
              countries {
                code
                name
              }
            }
        """

        self.graphql_request(query=query, variable={}, name="countries")

    @task(0)
    def get_languages(self):
        query = """
            {
              continents {
                code
                name
                countries{
                  code,
                  phone,
                  languages{
                    code,
                    name,
                    native
                  },
                  capital
                }
              }
            }
        """
        self.graphql_request(query=query, variable={}, name="languages")

    @task(0)
    def get_asia_countries(self):
        query = """
            {
              continent(code: "AS"){
                code,
                name,
                countries{
                  name
                }
              }
            }
        """

        self.graphql_request(query=query, variable={}, name="asia")

    @task(0)
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

        self.graphql_request(query=query, variable={}, name="countries")

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

        self.graphql_request(query=query, variable=variable, name="countries")


class UserTest(HttpUser):
    # host = "http://countries.trevorblades.com/"
    host = "http://178.128.106.241:30644/graphql"
    tasks = [UserTask1]
    wait_time = between(1, 2)
