//https://gitgraphjs.com/v1/examples/gitflowsupport.html
document.addEventListener('DOMContentLoaded', (event) => {
    toggleGraph();
});
const main = {
    master: {
        index: 0,
        name: "master"
    },
    develop: {
        index: 3,
        name: "develop"
    },
    feature: {
        index: 4,
        name: "feature"
    },
    release: {
        index: 2,
        name: "releases"
    },
    hotfix: {
        index: 1,
        name: "hotfix"
    }
};
const arrowsConfig = {
    colors: [
        "#4e79a7",
        "#f28e2c",
        "#e15759",
        "#76b7b2",
        "#59a14f",
        "#edc949",
        "#af7aa1",
        "#ff9da7",
        "#9c755f",
        "#bab0ab"
    ], // branches colors, 1 per column
    branch: {
        lineWidth: 3,
        spacingX: 60,
        mergeStyle: "straight",
        showLabel: true,
        labelFont: "normal 14pt Courier New",
        labelRotation: 0 // display branch names on graph
    },
    commit: {
        spacingY: -60,
        dot: {
            size: 6
        },
        message: {
            displayAuthor: false,
            displayBranch: true,
            displayHash: true,
            font: "normal 12pt Arial"
        },
        shouldDisplayTooltipsInCompactMode: "true",
        tooltipHTMLFormatter: function(commit) {
            return "" + commit.sha1 + "" + ": " + commit.message;
        }
    },
    arrow: {
        size: 12,
        offset: 3,
    }
};

const plainConfig = {
    colors: [
        "#4e79a7",
        "#f28e2c",
        "#e15759",
        "#76b7b2",
        "#59a14f",
        "#edc949",
        "#af7aa1",
        "#ff9da7",
        "#9c755f",
        "#bab0ab"
    ], // branches colors, 1 per column
    branch: {
        lineWidth: 8,
        spacingX: 50,
        showLabel: true,
        labelFont: "normal 14pt Courier New",
        labelRotation: 0 // display branch names on graph
    },
    commit: {
        spacingY: -80,
        dot: {
            size: 12
        },
        message: {
            displayAuthor: false,
            displayBranch: true,
            displayHash: true,
            font: "normal 12pt Arial"
        },
        shouldDisplayTooltipsInCompactMode: "true",
        tooltipHTMLFormatter: function(commit) {
            return "" + commit.sha1 + "" + ": " + commit.message;
        }
    }
};
let arrows = false;
const toggleGraph = function() {
    var myTemplate = (arrows) ? new GitGraph.Template(arrowsConfig) : new GitGraph.Template(plainConfig);
    if (document.getElementById("graph")) {
        document.getElementById("graph").remove();
    }
    let canvas = document.createElement("canvas");
    canvas.id = "graph";
    document.getElementById("graph-container").appendChild(canvas);
    draw(myTemplate);
    arrows = !arrows;
}

const draw = function(myTemplate) {


    const gitgraph = new GitGraph({
        orientation: "vertical",
        author: "Username",
        elementId: "graph",
        initCommitOffsetX: 0,
        initCommitOffsetY: 0,
        mode: "extended", // or compact if you don't want the messages
        template: myTemplate
    });

    const master = gitgraph.branch("master");
    master.commit({ message: "Initial Commit" });

    const develop = gitgraph.branch({
        parentBranch: master,
        name: "develop",
        column: main["develop"]["index"]
    });
    develop.commit({ message: "Setting up pipelines", author: "Hello" });
    const developCommit = {
        messageDisplay: false,
    };
    develop.commit(developCommit);
    const hotFix = function(name, parent) {
        return gitgraph.branch({
            parentBranch: parent,
            name: name,
            column: main["hotfix"]["index"]
        });
    };
    const addFeature = function(name) {
        return gitgraph.branch({
            parentBranch: develop,
            name: `feature/${name}`,
            column: main["feature"]["index"]
        });
    };
    const aFeature = gitgraph.branch({
        parentBranch: develop,
        name: "feature/cool-stuff",
        column: main["feature"]["index"]
    });
    develop.commit(developCommit);
    aFeature.commit({ message: "Making it work" });
    aFeature.commit({ message: "Completed work" });
    aFeature.merge(develop);
    develop.commit(developCommit);
    const release = gitgraph.branch({
        parentBranch: develop,
        name: "releases/1.0.0",
        column: main["release"]["index"] // which column index it should be displayed in
    });

    develop.commit(developCommit);

    release.commit({
        message: "Start v1.0.0-rc Release Candidate builds",
        tag: "1.0.0-rc1"
    });

    const bFeature = addFeature("next-feature")
        .commit({ message: "Starting work on feature for next release" })
        .commit("Work")
        .commit("Work work work")


    release.commit({ message: "Minor bug fixing allowed on release branch." });

    release.commit({ message: "Release candidate 2", tag: "1.0.0-rc2" });

    release.merge(master, { message: "Release v1.0.0 tagged", tag: "1.0.0" });

    master.merge(develop, {
        message: "Updating development with minor fix done on release branch"
    });

    bFeature.merge(develop);
    develop.commit(developCommit);
    const patch = hotFix("hotfix/critical-bug", master).commit("Hotfix for production bug")



    patch.merge(master, {
        tag: "1.0.1"
    })
    patch.merge(develop, {
        message: "Incorporate bug fix"
    })
    const release2 = gitgraph.branch({
        parentBranch: develop,
        name: "releases/1.1.1",
        column: main["release"]["index"] // which column index it should be displayed in
    });

    release2.commit({ message: 'changing css' }).commit({ message: 'Release candidate 2', tag: '1.1.1-rc2' })
    develop.commit()
    release2.merge(master, { tag: '1.1.1' });
    master.merge(develop)
}