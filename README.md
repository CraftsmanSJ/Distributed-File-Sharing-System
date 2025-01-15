# Distributed File Sharing System  

## Project Overview  
This project implements a **Distributed File Sharing System** using **Peer-to-Peer (P2P) Communication**. The system allows peers to share files efficiently by dividing them into chunks,
distributing them among peers, and reassembling them on the receiving end. This approach ensures scalability, fault tolerance, and efficient file distribution across the network.  

## Features  
1. **File Chunking and Distribution**  
   - Files are divided into smaller chunks to enable parallel transfer and efficient use of network resources.  
2. **Peer-to-Peer Communication**  
   - Direct communication between peers without relying on a centralized server.  
3. **Distributed File Storage**  
   - File chunks are stored across multiple peers in the network.  
4. **Dynamic Peer Discovery**  
   - Peers can dynamically join or leave the network without disrupting ongoing transfers.  
5. **Efficient File Retrieval**  
   - The requesting peer collects chunks from multiple peers simultaneously and reassembles the original file.  
6. **Fault Tolerance**  
   - If a peer becomes unavailable during a transfer, the system fetches the missing chunks from other peers.  

## How It Works  
1. **File Chunking:**  
   - When a peer shares a file, it is divided into fixed-sized chunks and assigned unique identifiers (hash values).  

2. **Chunk Distribution:**  
   - Chunks are distributed to multiple peers in the network. Metadata about which peer holds which chunk is updated in the system.  

3. **Peer Communication:**  
   - Peers communicate using a P2P protocol. Each peer maintains a list of active peers and the chunks they possess.  

4. **File Request and Retrieval:**  
   - A peer requesting a file broadcasts a request. Peers with relevant chunks respond, and the requesting peer downloads the chunks simultaneously from multiple sources.  

5. **Reassembly:**  
   - Once all chunks are received, the file is reassembled in its original form.  

6. **Fault Tolerance:**  
   - If a peer fails to send a chunk, the system retries by fetching the chunk from an alternate peer.  
