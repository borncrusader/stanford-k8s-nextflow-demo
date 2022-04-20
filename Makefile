clean:
	kubectl delete pod pp-00 --force
	kubectl delete pod pp-01 --force
	kubectl delete pod pp-02 --force
	kubectl delete pod models --force
