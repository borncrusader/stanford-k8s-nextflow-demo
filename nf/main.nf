#!/usr/bin/env nextflow
nextflow.enable.dsl=2 

root = params.in

process pp_00 {
    input:
    val root_in
    output:
    val root_out

    """
    kubectl apply -f $root_in/k8s/pod-pp-00.yaml

    sleep 5
# TODO(srinath): try to see if this can be in the yaml
    kubectl port-forward pod/pp-00 5000 &

    while [ /bin/true ]; do
        sleep 5

        curl http://localhost:5000/status 2>/dev/null 1> result
        if grep DONE result; then
            root_out=$root_in
            break
        fi
    done

    kubectl delete pod pp-00 --force

    kill %%

    echo "done"
    """
}

process pp_01 {
    input:
    val root_in
    output:
    val root_out

    """
    kubectl apply -f $root_in/k8s/pod-pp-01.yaml

    sleep 5
# TODO(srinath): try to see if this can be in the yaml
    kubectl port-forward pod/pp-01 5000 &

    while [ /bin/true ]; do
        sleep 5

        curl http://localhost:5000/status 2>/dev/null 1> result
        if grep DONE result; then
            root_out=$root_in
            break
        fi
    done

    kubectl delete pod pp-01 --force

    kill %%

    echo "done"
    """
}

workflow {
    log.info "starting preprocessing routines; pwd: $root"

    pp_00(root)
    pp_01(pp_00.out)
    pp_01.out.view()
}

workflow.onComplete {
    log.info "done"
}
