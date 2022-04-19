#!/usr/bin/env nextflow
nextflow.enable.dsl=2 

root = params.in

process pp_00 {
    input:
    val in
    output:
    env out

    shell:
    """
    kubectl apply -f $in/k8s/pod-pp-00.yaml

    sleep 5
# TODO(srinath): try to see if this can be in the yaml
    kubectl port-forward pod/pp-00 5000 &

    while [ /bin/true ]; do
        sleep 5

        curl http://localhost:5000/status 2>/dev/null 1> result
        if grep DONE result; then
            echo "breaking"
            break
        fi
    done

    kill %%

    export out=$in
    """
}

process pp_01 {
    input:
    val in
    output:
    env out

    shell:
    """
    kubectl apply -f $in/k8s/pod-pp-01.yaml

    sleep 5
# TODO(srinath): try to see if this can be in the yaml
    kubectl port-forward pod/pp-01 5000 &

    while [ /bin/true ]; do
        sleep 5

        curl http://localhost:5000/status 2>/dev/null 1> result
        if grep DONE result; then
            break
        fi
    done

    export out=$in
    """
}

process pp_02 {
    input:
    val in
    output:
    env out

    shell:
    """
    kubectl apply -f $in/k8s/pod-pp-02.yaml

    sleep 5
# TODO(srinath): try to see if this can be in the yaml
    kubectl port-forward pod/pp-02 5000 &

    while [ /bin/true ]; do
        sleep 5

        curl http://localhost:5000/status 2>/dev/null 1> result
        if grep DONE result; then
            break
        fi
    done

    export out=$in
    """
}

workflow {
    log.info "starting preprocessing routines; pwd: $root"

    log.info "starting pp-00"
    pp_00(root)

    log.info "starting pp-01"
    pp_01(pp_00.out)

    pp_01.out.view()
}

workflow.onComplete {
    log.info "done"
}
