output "cluster_name" {
  description = "Nom du cluster GKE créé"
  value       = google_container_cluster.primary.name
}

output "cluster_endpoint" {
  description = "Endpoint de l'API Kubernetes"
  value       = google_container_cluster.primary.endpoint
}

output "node_pool_name" {
  description = "Nom du node pool principal"
  value       = google_container_node_pool.primary_nodes.name
}

output "vpc_name" {
  description = "Nom du réseau VPC utilisé"
  value       = google_compute_network.vpc_network.name
}
