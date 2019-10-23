import driver_class as driver
import numpy as np

# Bring in all the data needed to execute the orders
weights = np.genfromtxt("/Users/spencerseliga/Desktop/newnetwork.csv", delimiter=',')
wait_list = np.genfromtxt("/Users/spencerseliga/Desktop/newrequests.csv", delimiter=',', dtype=int)

#This function is used to delete an order from the existing queue
def delete_order(queue, order):
    if len(queue[order[0]]) > 1:
        for i in range(0, len(queue[order[0]])):
            if queue[order[0]][i] == order[1]:
                del queue[order[0]][i]
                break
    else:
        del queue[order[0]]
    return queue
#This function is used to add all orders to the queue that have not already been added.
def add_orders(queue, wait_data, curr_time, old_curr_time):
    #For each order in wait_data
    for order in wait_data:
        #If the time stamp is greater then the last time we added order, or less then the current time.
        if old_curr_time < order[0] <= curr_time:
            if order[0] in queue:
                queue[order[0]] += [(order[1], order[2])]
            else:
                queue[order[0]] = [(order[1], order[2])]
        elif order[0] == 0 and curr_time ==0:
            if order[0] in queue:
                queue[order[0]] += [(order[1], order[2])]
            else:
                queue[order[0]] = [(order[1], order[2])]
    return queue
#this function is used to find the order in the queue which has the shortest path to drive to
def find_short(Q, pos, queue):
    #define min_dist as a large number, and init min as 0
    min_dist = 1000
    min = 0
    #for each item in the current queue
    for item in queue:
        #if there are more then 1 item under that timestamp, loop through each item.
        if len(queue[item]) > 1:
            #for each item with the same stamp.
            for item_2 in queue[item]:
                #See if any are the min items.
                temp = item_2[0]
                ub = driver.uber_driver()
                temp_dist = ub.dijkstra(Q, pos, temp)
                if temp_dist < min_dist:
                    min_dist = temp_dist
                    min = (item, item_2)
        else:
            temp = queue[item][0][0]
            ub = driver.uber_driver()
            temp_dist = ub.dijkstra(Q, pos, temp)
            if temp_dist < min_dist:
                min_dist = temp_dist
                min = (item, queue[item][0])
    #Above section is finding the minimum order.
    return min

#-------- Implementation of the code using a priority queue based off distance to the pickup -------------

#Initialize all variable for this implementation of the algorithm
curr_time = 0
start_pos = 1
old_curr_time = 0
queue = {}
tot_wait_time = 0

#Execute the orders in terms of which pickup location is closest to the previous drop off.
while(True):
    #Add any orders to the queue. Only take into consideration orders that have happened since the last time you added,
    #but also none that are in the future.
    queue = add_orders(queue, wait_list, curr_time, old_curr_time)
    #Keep track of the last time you added to the queue
    old_curr_time = curr_time

    #If the queue is empty, tck current_time up by one, and check again.
    #if it isn't empty, find what order you want to execute.
    if queue != {}:
        # Find the shortest path in the queue
        order = find_short(weights, start_pos, queue)

        # Delete the order from the queue, and begin processing it.
        queue = delete_order(queue, order)

        # Set all appropriate metrics, to start
        order_time = order[0]
        order_location = order[1]

        # From tuple, seperate into pickup and dropoff
        pickup = order_location[0]
        dropoff = order_location[1]

        # Drive to the pickup location
        ub = driver.uber_driver()
        trip_time = ub.dijkstra(weights, start_pos, pickup)
        # Keep track of the time elapsed
        curr_time += trip_time
        #Calculate the wait time the user experienced.
        wait_time = curr_time - order_time
        #Add that wait time to the running tally.
        tot_wait_time += wait_time


        # Now at the location, pickup the passenger
        start_pos = pickup
        end_pos = dropoff

        # Make the trip to the pickup locations
        ub = driver.uber_driver()
        trip_time = ub.dijkstra(weights, start_pos, end_pos)
        # Record how long it took for the time.
        curr_time = trip_time + curr_time

        # Once the person is dropped off, reset location, and move onto the next order.
        start_pos = end_pos
    else:
        curr_time += 1

    #If the current time has exceeded 4000, the driver has finished his shift, and the algorithm is done.
    if curr_time > 4000:
        break
customers = len(wait_list)
avg = tot_wait_time/customers
print customers
print "The total wait time using a distance queue for all the customers is: " + str(tot_wait_time) + " mins"
print "This is an average wait time of: " + str(avg) + " mins"















