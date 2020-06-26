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
const myTemplateConfig = {
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
        lineWidth: 6,
        spacingX: 40,
        spacingY: -40,
        showLabel: true,
        labelFont: "normal 10pt Courier New",
        labelRotation: 0 // display branch names on graph
    },
    commit: {
        spacingX: 40,
        spacingY: -40,
        dot: {
            size: 6
        },
        message: {
            displayAuthor: false,
            displayBranch: true,
            displayHash: true,
            font: "normal 10pt Arial"
        },
        shouldDisplayTooltipsInCompactMode: "true",
        tooltipHTMLFormatter: function(commit) {
            return "" + commit.sha1 + "" + ": " + commit.message;
        }
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
        spacingX: 40,
        mergeStyle: "straight",
        showLabel: true,
        labelFont: "normal 10pt Courier New",
        labelRotation: 0 // display branch names on graph
    },
    commit: {
        spacingX: 40,
        spacingY: -40,
        dot: {
            size: 6
        },
        message: {
            displayAuthor: false,
            displayBranch: true,
            displayHash: true,
            font: "normal 10pt Arial"
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
arrows = false;
var myTemplate = (arrows) ? new GitGraph.Template(arrowsConfig) : new GitGraph.Template(myTemplateConfig);
const createDev = function(graph, parent) {
    return graph.branch({
        parentBranch: parent,
        name: "develop",
        column: main["develop"]["index"]
    });
};
const addhotFix = function(graph, name, parent) {
    return graph.branch({
        parentBranch: parent,
        name: `hotfix/${name}`,
        column: main["hotfix"]["index"]
    });
};
const addFeature = function(graph, name, parent) {
    return graph.branch({
        parentBranch: parent,
        name: `feature/${name}`,
        column: main["feature"]["index"]
    });
};

const addNextFeature = function(graph, name, parent) {
    return graph.branch({
        parentBranch: parent,
        name: `feature/${name}`,
        column: main["feature"]["index"] + 1
    });
};

const addRelease = function(graph, name, parent) {
    return graph.branch({
        parentBranch: parent,
        name: `release/${name}`,
        column: main["release"]["index"] // which column index it should be displayed in
    });
};
const createSecond = function() {
    const second = new GitGraph({
        orientation: "horizontal",
        author: "Username",
        elementId: "second",
        initCommitOffsetX: 0,
        initCommitOffsetY: 0,
        mode: "extended", // or compact if you don't want the messages
        template: myTemplate
    });
    const secondMast = second.branch("master");

    secondMast.commit({ message: "initial commit", tag: "1.0.0" });

    const firstHot = addhotFix(second, "breaking-bug", secondMast)
        .commit()
        .commit();

    secondDev = createDev(second, secondMast).commit();

    firstHot.merge(secondMast, { tag: "1.0.1" });
    firstHot.merge(secondDev);
}

const createFirst = function() {
    const first = new GitGraph({
        orientation: "horizontal",
        author: "Username",
        elementId: "first",
        initCommitOffsetX: 0,
        initCommitOffsetY: 0,
        mode: "extended", // or compact if you don't want the messages
        template: myTemplate
    });

    const firstMast = first.branch("master");

    firstMast.commit({ message: "initial commit", tag: "0.0.0" });

    const firstDev = createDev(first, firstMast);

    firstDev.commit();
    firstFeat = addFeature(first, "amazing-stuff", firstDev);

    firstFeat.commit();
    firstDev.commit();
    secondFeat = addNextFeature(first, "shiny-things", firstDev).commit();
    firstFeat.commit();
    firstFeat.merge(firstDev);
    firstRel = addRelease(first, "1.0.0", firstDev).commit({ tag: "1.0.0-rc1" });
    secondFeat.merge(firstDev);
    firstRel.commit();
    firstRel.merge(firstMast, { tag: "1.0.0" });
    firstMast.merge(firstDev);
    firstDev.commit();
};