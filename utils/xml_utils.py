import re
import xml.etree.ElementTree as ElementTree


def find_in_file(xml_path, x_paths, ignore_namespaces=True):
    """
    :type xml_path: str
    :type x_paths: list
    :type ignore_namespaces: bool
    :rtype: dict
    """
    tree = ElementTree.parse(xml_path)
    root = tree.getroot()
    return find_in_tree(root, x_paths, ignore_namespaces)


def find_in_string(xml_string, x_paths, ignore_namespaces=True):
    root_element = ElementTree.fromstring(xml_string)
    return find_in_tree(root_element, x_paths, ignore_namespaces)


def find_in_tree(root_element, x_paths, ignore_namespaces):
    elements_dict = gather_elements(root_element, x_paths, ignore_namespaces)

    result = {}

    for x_path, elements in elements_dict.items():
        if (elements is not None) and elements:
            if len(elements) == 1:
                result[x_path] = read_element(elements[0])
            else:
                result[x_path] = [read_element(element) for element in elements]
        else:
            result[x_path] = None

    return result


def gather_elements(root_element, x_paths, ignore_namespaces):
    root_ns = namespace(root_element)
    ns = {}

    if root_ns and ignore_namespaces:
        ns["x"] = root_ns

    result = {}

    for x_path in x_paths:
        search_path = x_path

        if root_ns and ignore_namespaces:
            search_path = adapt_namespace(x_path, "x")

        elements = root_element.findall(search_path, ns)
        if (elements is not None) and elements:
            result[x_path] = elements
        else:
            result[x_path] = None

    return result


def read_element(element):
    attributes_map = dict(element.attrib)

    sub_elements = list(element)
    if len(sub_elements) > 0:
        as_map = {}
        for sub_element in sub_elements:
            key = sub_element.tag
            key = key[key.rfind("}") + 1:]

            value = read_element(sub_element)

            if (key in as_map):
                if isinstance(as_map[key], list):
                    value_list = as_map[key]
                else:
                    value_list = [as_map[key]]
                    as_map[key] = value_list

                value_list.append(value)

            else:
                as_map[key] = value

        if attributes_map:
            as_map.update(attributes_map)

        return as_map
    else:
        if element.text:
            if attributes_map:
                attributes_map['text'] = element.text.strip()
                return attributes_map

            return element.text.strip()

        else:
            if attributes_map:
                return attributes_map

            return ''


def namespace(element):
    m = re.match('\{(.*)\}', element.tag)
    return m.group(1) if m else ''


def adapt_namespace(x_path, prefix):
    path_elements = x_path.split("/")

    result = []

    for element in path_elements:
        if element == '*':
            result.append(element)
            continue

        result.append(prefix + ":" + element)

    return "/".join(result)


def replace_in_tree(file_path, replace_dict, ignore_namespaces=True):
    tree = ElementTree.parse(file_path)
    elements_dict = gather_elements(tree.getroot(), replace_dict.keys(), ignore_namespaces)

    for xpath, elements in elements_dict.items():
        if elements is None:
            continue

        value = replace_dict[xpath]

        if isinstance(elements, list):
            for element in elements:
                element.text = value
        else:
            elements.text = value

    tree.write(file_path)
