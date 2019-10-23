import heapq

class uber_driver():

    def dijkstra(self, Q, start, end):
        # Start by making a large number called INF
        INF = 10000000

        #Create a dictionary to store all the previous node of the node that is being visited
        #Initialize them as leading to themselves to start.
        prev = {}
        for q in range(1, len(Q)):
            prev[q] = q

        #Create a dictionary of all nodes storing the minimum distance from that node to the source node.
        #Initialize them all as INF so that every path will be less then that.
        dist = {}
        for n in range(1, len(Q)+1):
            dist[n] = INF
        # Make the distance from the source node to itself as 0
        dist[start] = 0

        #Start by making a priority queue, and pushing the first source node, and its distance to itself
        #onto the priority queue
        qu = []
        heapq.heappush(qu, ([dist[start], start]))

        #Start the process of looking for the smallest path. to the end node.
        #This while loop will run until the queue is empty, and every path search has been exhausted.
        while(qu):
            #take off the highest priority (smallest path) from the top of the queue
            u = heapq.heappop(qu)

            #Define your current_distance from the source node, and current node_id
            cur_dist = u[0]
            cur_id = u[1]
            #check make sure your current distance is equal to the stored distance you ahve from the node.
            if cur_dist == dist[cur_id]:
                # if your current node is the same as your end node, you can break the while loop.
                # You have found your minimal path.
                if cur_id == end:
                    break

                # Next define neighbour to be all the current nodes neighbours.
                neighbour = {}
                index = 0
                for i in Q[cur_id-1 , :]:
                    index += 1
                    #Store every other node it commmunicates with in neighbour, by the key of what node they are.
                    if i > 0:
                        neighbour[index] = i

                # Start to loop through all the neighbours weights, and assign them to the priority queue.
                #Once pushed onto the queue, the queue will resort in order of priority,
                # thus pulling the minimal path to the top.
                for i in neighbour:
                    next_id = i
                    neighbour_weight = neighbour[i]
                    #check to make sure that you have the smallest path leading to that node.
                    ## If you have found a larger path, do not add it to the heap.
                    if dist[cur_id] + neighbour_weight < dist[next_id]:
                        #assign the new smallest path to the "next_id" node
                        dist[next_id] = dist[cur_id] + neighbour_weight
                        #push it onto the priority queue
                        heapq.heappush(qu, [dist[next_id], next_id])
                        #set the "next_id's" previous node to the current node.
                        prev[next_id] = cur_id
            #REPEAT THIS PROCESS POPPING THE NEXT MINIMAL PATH OFF THE QUEUE, AND PURSUING
            #THE PATH UNTIL YOU FIND THE END NODE.


        # If the distance at the end is INF, there was no path found to it.
        if dist[end] == INF:
            print "No possible path is found, skip to next order"
            return 0
        #otherwise, a possible path has been found.
        else:
            #init final variables
            wait = 0
            path = []
            node = end

            #Draw the path the uber took, and calculate the wait time
            # by adding the relative paths from node to node.
            while(True):
                path.append(node)
                if node == start:
                    break
                wait = wait + Q[node-1, prev[node]-1]
                node = prev[node]
        #return your wait time for the trip.
        #print path
        return wait
