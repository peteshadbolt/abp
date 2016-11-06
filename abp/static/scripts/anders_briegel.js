var abj = {};
abj.node = {};
abj.adj = {};

abj.add_node = function(node, meta) {
    if (meta === undefined){meta = {};}
    abj.adj[node] = {};
    abj.node[node] = {};
    abj.node[node].vop = tables.clifford.hadamard;
    Object.assign(abj.node[node], meta);
};

abj.add_nodes = function(nodes) {
    nodes.forEach(add_node);
};

abj.del_node = function(node) {
    for (var i in abj.adj[node]) {
        abj.del_edge(node, i);
    }
    delete abj.node[node];
};

abj.add_edge = function(a, b) {
    abj.adj[a][b] = {};
    abj.adj[b][a] = {};
};

abj.add_edges = function(edges) {
    edges.forEach(function(e) {
        add_edge(e[0], e[1]);
    });
};

abj.del_edge = function(a, b) {
    delete abj.adj[a][b];
    delete abj.adj[b][a];
};

abj.has_edge = function(a, b) {
    return Object.prototype.hasOwnProperty.call(abj.adj[a], b);
};

abj.is_sole_member = function(group, node) {
    // TODO: this is slow as heck
    var keys = Object.keys(group);
    return keys.length == 1 && keys[0] == node;
};

abj.update = function(newState) {
    abj.node = newState.node;
    abj.adj = newState.adj;
};

abj.order = function(){
    return Object.keys(abj.node).length;
};

abj.edgelist = function() {
    var seen = {};
    var output = [];
    for (var i in abj.adj) {
        for (var j in abj.adj[i]) {
            if (!Object.prototype.hasOwnProperty.call(seen, j)) {
                output.push([i, j]);
            }
        }
        seen[i] = true;
    }
    return output;
};


