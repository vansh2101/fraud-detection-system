import http.client
import json

# To not request data from API every time, I saved the data in a file

# def load_pnr_data(pnrNumber):
#     # Check if the file exists
#     if os.path.exists("pnr_data.json"):
#         with open("pnr_data.json", "r") as file:
#             data = json.load(file)
#             # Return data if PNR is found
#             if pnrNumber in data:
#                 return data[pnrNumber]
#     return None

# def save_pnr_data(pnrNumber, data):
#     # Load existing data or create a new dictionary
#     if os.path.exists("pnr_data.json"):
#         with open("pnr_data.json", "r") as file:
#             all_data = json.load(file)
#     else:
#         all_data = {}

#     # Add new PNR data
#     all_data[pnrNumber] = data

#     # Save updated data back to file
#     with open("pnr_data.json", "w") as file:
#         json.dump(all_data, file)

# def fetch_pnr_data_from_api(pnrNumber):
#     # API connection setup
#     conn = http.client.HTTPSConnection("irctc-indian-railway-pnr-status.p.rapidapi.com")
#     headers = {
#         'x-rapidapi-key': "8cf5277da0mshf45e48dbcd767f8p138d15jsn36eb177ca5fd",
#         'x-rapidapi-host': "irctc-indian-railway-pnr-status.p.rapidapi.com"
#     }
#     # Make the API request
#     conn.request("GET", f"/getPNRStatus/{pnrNumber}", headers=headers)
#     res = conn.getresponse()
#     data = res.read()
#     return json.loads(data.decode("utf-8"))


def isSpam(
    pnrNumber, dateOfJourney, trainNumber, trainName, sourceStation, destinationStation,
    reservationUpto, boardingPoint, journeyClass, numberOfPassengers, chartStatus,
    passengerDetails, trainCancelStatus, bookingFare, ticketFare, quota, reasonType,
    ticketTypeInPrs, bookingDate, arrivalDate, distance, isWL
):
    reasons = []
    # # API connection setup
    # api_data = load_pnr_data(pnrNumber)
    # if not api_data:
    #     response = fetch_pnr_data_from_api(pnrNumber)
    #     if not response.get('success', False):
    #         print("PNR doesn't exist")
    #         return True  # Mark as spam if API request fails
    #     api_data = response['data']
    #     # Save fetched data for future use
    #     save_pnr_data(pnrNumber, api_data)

    # **********************************************************
    # *********************************************************
    conn = http.client.HTTPSConnection("irctc-indian-railway-pnr-status.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "8cf5277da0mshf45e48dbcd767f8p138d15jsn36eb177ca5fd",
        'x-rapidapi-host': "irctc-indian-railway-pnr-status.p.rapidapi.com"
    }

    # Make the API request
    conn.request("GET", f"/getPNRStatus/{pnrNumber}", headers=headers)
    res = conn.getresponse()
    data = res.read()

    # Decode and load response JSON
    response = json.loads(data.decode("utf-8"))

    # Check if response is successful
    if not response.get('success', False):
        print(response["message"])
        return True

    # Get API data
    api_data = response['data']

    # Validate each non-None field in API data
    conditions = [
        (dateOfJourney is None or api_data['dateOfJourney'] == dateOfJourney, "dateOfJourney mismatch"),
        (trainNumber is None or api_data['trainNumber'] == trainNumber, "trainNumber mismatch"),
        (trainName is None or api_data['trainName'] == trainName, "trainName mismatch"),
        (sourceStation is None or api_data['sourceStation'] == sourceStation, "sourceStation mismatch"),
        (destinationStation is None or api_data['destinationStation'] == destinationStation, "destinationStation mismatch"),
        (reservationUpto is None or api_data['reservationUpto'] == reservationUpto, "reservationUpto mismatch"),
        (boardingPoint is None or api_data['boardingPoint'] == boardingPoint, "boardingPoint mismatch"),
        (journeyClass is None or api_data['journeyClass'] == journeyClass, "journeyClass mismatch"),
        (numberOfPassengers is None or api_data['numberOfpassenger'] == numberOfPassengers, "numberOfPassengers mismatch"),
        (chartStatus is None or api_data['chartStatus'] == chartStatus, "chartStatus mismatch"),
        (trainCancelStatus is None or api_data['trainCancelStatus'] == trainCancelStatus, "trainCancelStatus mismatch"),
        (bookingFare is None or api_data['bookingFare'] == bookingFare, "bookingFare mismatch"),
        (ticketFare is None or api_data['ticketFare'] == ticketFare, "ticketFare mismatch"),
        (quota is None or api_data['quota'] == quota, "quota mismatch"),
        (reasonType is None or api_data['reasonType'] == reasonType, "reasonType mismatch"),
        (ticketTypeInPrs is None or api_data['ticketTypeInPrs'] == ticketTypeInPrs, "ticketTypeInPrs mismatch"),
        (bookingDate is None or api_data['bookingDate'] == bookingDate, "bookingDate mismatch"),
        (arrivalDate is None or api_data['arrivalDate'] == arrivalDate, "arrivalDate mismatch"),
        (distance is None or api_data['distance'] == distance, "distance mismatch"),
        (isWL is None or api_data['isWL'] == isWL, "isWL mismatch")
    ]

    # Check each condition and append the reason if it fails
    for condition, reason in conditions:
        if not condition:
            reasons.append(reason)

    # Check passenger details, if provided
    if passengerDetails:
        for i, passenger in enumerate(passengerDetails):
            if i >= len(api_data['passengerList']):
                reasons.append("More passengers provided than in the API data")
                break

            passenger_api = api_data['passengerList'][i]

            # Append conditions for each passenger attribute
            passenger_conditions = [
                (passenger.get('passengerFoodChoice') is None or
                 passenger_api['passengerFoodChoice'] == passenger['passengerFoodChoice'], f"Passenger {i + 1} passengerFoodChoice mismatch"),
                (passenger.get('concessionOpted') is None or
                 passenger_api['concessionOpted'] == passenger['concessionOpted'], f"Passenger {i + 1} concessionOpted mismatch"),
                (passenger.get('passengerIcardFlag') is None or
                 passenger_api['passengerIcardFlag'] == passenger['passengerIcardFlag'], f"Passenger {i + 1} passengerIcardFlag mismatch"),
                (passenger.get('childBerthFlag') is None or
                 passenger_api['childBerthFlag'] == passenger['childBerthFlag'], f"Passenger {i + 1} childBerthFlag mismatch"),
                (passenger.get('passengerNationality') is None or
                 passenger_api['passengerNationality'] == passenger['passengerNationality'], f"Passenger {i + 1} passengerNationality mismatch"),
                (passenger.get('passengerQuota') is None or
                 passenger_api['passengerQuota'] == passenger['passengerQuota'], f"Passenger {i + 1} passengerQuota mismatch"),
                (passenger.get('passengerCoachPosition') is None or
                 passenger_api['passengerCoachPosition'] == passenger['passengerCoachPosition'], f"Passenger {i + 1} passengerCoachPosition mismatch"),
                (passenger.get('waitListType') is None or
                 passenger_api['waitListType'] == passenger['waitListType'], f"Passenger {i + 1} waitListType mismatch"),
                (passenger.get('bookingStatus') is None or
                 passenger_api['bookingStatus'] == passenger['bookingStatus'], f"Passenger {i + 1} bookingStatus mismatch"),
                (passenger.get('bookingCoachId') is None or
                 passenger_api['bookingCoachId'] == passenger['bookingCoachId'], f"Passenger {i + 1} bookingCoachId mismatch"),
                (passenger.get('bookingBerthNo') is None or
                 passenger_api['bookingBerthNo'] == passenger['bookingBerthNo'], f"Passenger {i + 1} bookingBerthNo mismatch"),
                (passenger.get('bookingBerthCode') is None or
                 passenger_api['bookingBerthCode'] == passenger['bookingBerthCode'], f"Passenger {i + 1} bookingBerthCode mismatch"),
                (passenger.get('bookingStatusDetails') is None or
                 passenger_api['bookingStatusDetails'] == passenger['bookingStatusDetails'], f"Passenger {i + 1} bookingStatusDetails mismatch"),
                (passenger.get('currentStatus') is None or
                 passenger_api['currentStatus'] == passenger['currentStatus'], f"Passenger {i + 1} currentStatus mismatch"),
                (passenger.get('currentCoachId') is None or
                 passenger_api['currentCoachId'] == passenger['currentCoachId'], f"Passenger {i + 1} currentCoachId mismatch"),
                (passenger.get('currentBerthNo') is None or
                 passenger_api['currentBerthNo'] == passenger['currentBerthNo'], f"Passenger {i + 1} currentBerthNo mismatch"),
                (passenger.get('currentBerthCode') is None or
                 passenger_api['currentBerthCode'] == passenger['currentBerthCode'], f"Passenger {i + 1} currentBerthCode mismatch"),
                (passenger.get('currentStatusDetails') is None or
                 passenger_api['currentStatusDetails'] == passenger['currentStatusDetails'], f"Passenger {i + 1} currentStatusDetails mismatch")
            ]

            for condition, reason in passenger_conditions:
                if not condition:
                    reasons.append(reason)

    # If there are reasons, mark as spam
    is_spam = len(reasons) > 0
    return is_spam, reasons


# Test the function
# print(isSpam("2221748570", None, "22425", "VANDE BHARAT EXP", "AYC", "ANVT", "ANVT", "AYC", "CC", 1, None, None, None, None, None, None, None, None, None, None, None, None))